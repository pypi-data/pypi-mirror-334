from __future__ import annotations

import typing
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path

import f90nml
import matplotlib.pyplot as plt
import music_mesa_tables as mmt
import numpy as np
import pandas as pd
from loam.base import ConfigBase, Section, entry
from loam.tools import path_entry
from numpy.typing import NDArray
from rich import box, progress
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.text import Text
from scipy.optimize import fsolve

from .constants import REVISIONS, PhysConsts
from .fgong import FgongModel
from .format2 import Header, MusicNewFormatDumpFile

if typing.TYPE_CHECKING:
    from .cli import CliConfig


@dataclass
class Grid(Section):
    ncells_radius: int = entry(val=512, doc="number of cells in radial direction")
    radius_min: float = entry(val=0.1, doc="internal r bound (relative to Rstar)")
    radius_max: float = entry(val=0.9, doc="external r bound (relative to Rstar)")
    ncells_theta: int = entry(val=512, doc="number of cells in theta direction")
    theta_deg_min: float = entry(val=0.0, doc="min theta in degree")
    theta_deg_max: float = entry(val=180.0, doc="max theta in degree")
    ncells_phi: int = entry(val=0, doc="number of cells in phi direction")
    phi_deg_min: float = entry(val=0.0, doc="min phi in degree")
    phi_deg_max: float = entry(val=360.0, doc="max phi in degree")


@dataclass
class Inversion(Section):
    eos_tol: float = entry(
        val=1e-10,
        doc="convergence tolerance for EoS inversion (e from p)",
    )
    n2_tol: float = entry(
        val=1e-10,
        doc="convergence tolerance for N2 inversion (rho from N2)",
    )


@dataclass
class MesaEos(Section):
    metallicity: float = entry(val=0.02, doc="metallicity for MESA EoS")
    he_mode: str = entry(
        val="active",
        doc='mode for Helium fraction, one of {"active", "frozen", "constant"}',
    )
    he_frac: float = entry(val=0.28, doc='value to use when he_mode="constant"')


@dataclass
class Physics(Section):
    nmom: int = entry(val=2, doc="number of momentum components")
    constants_revision: str = entry(
        val="CODATA2022",
        doc="revision of physical constants to use",
    )


@dataclass
class Sources(Section):
    fgong: Path = path_entry("model.fgong", doc="path to fgong model")
    nml_template: Path = path_entry(
        "params_template.nml", doc="MUSIC namelist to modify"
    )


@dataclass
class Output(Section):
    music_run_dir: Path = path_entry("run", "path to MUSIC run directory")
    ic: Path = path_entry(
        "ic.music",
        doc="path of generated music model, relative to `music_run_dir`",
    )
    nml: Path = path_entry(
        "params.nml",
        doc="modified MUSIC namelist, relative to `music_run_dir`",
    )


@dataclass
class Config(ConfigBase):
    grid: Grid
    inversion: Inversion
    mesa_eos: MesaEos
    physics: Physics
    sources: Sources
    output: Output


@dataclass(frozen=True)
class Geometry:
    r_faces: NDArray[np.float64]
    theta_faces: NDArray[np.float64]
    phi_faces: NDArray[np.float64] | None
    nmom: int
    r_star: float

    def __post_init__(self) -> None:
        assert 2 <= self.ndim <= self.nmom <= 3

    @cached_property
    def ndim(self) -> int:
        return 2 if self.phi_faces is None else 3

    @staticmethod
    def from_conf(grid: Grid, nmom: int, r_star: float) -> Geometry:
        if grid.ncells_phi > 1:
            pfaces = np.linspace(
                grid.phi_deg_min * np.pi / 180.0,
                grid.phi_deg_max * np.pi / 180.0,
                grid.ncells_phi + 1,
            )
            nmom = 3
        else:
            pfaces = None
            nmom = 3 if nmom >= 3 else 2
        return Geometry(
            r_faces=np.linspace(
                grid.radius_min * r_star,
                grid.radius_max * r_star,
                grid.ncells_radius + 1,
            ),
            theta_faces=np.linspace(
                grid.theta_deg_min * np.pi / 180.0,
                grid.theta_deg_max * np.pi / 180.0,
                grid.ncells_theta + 1,
            ),
            phi_faces=pfaces,
            nmom=nmom,
            r_star=r_star,
        )

    @cached_property
    def r_centers(self) -> NDArray[np.float64]:
        return face_to_center_with_gc(self.r_faces)


def face_to_center_with_gc(at_faces: NDArray[np.floating]) -> NDArray[np.floating]:
    at_centers = np.zeros(at_faces.size + 1)
    at_centers[1:-1] = (at_faces[:-1] + at_faces[1:]) / 2
    at_centers[0] = 2 * at_faces[0] - at_centers[1]
    at_centers[-1] = 2 * at_faces[-1] - at_centers[-2]
    return at_centers


def center_with_gc_to_faces(at_centers: NDArray[np.floating]) -> NDArray[np.floating]:
    return (at_centers[1:] + at_centers[:-1]) / 2


@dataclass(frozen=True)
class ThermoState:
    he: NDArray[np.float64]
    dens: NDArray[np.float64]
    p_target: NDArray[np.float64]
    eos: mmt.CstMetalEos
    tol: float

    @cached_property
    def e_int(self) -> NDArray[np.float64]:
        logp = np.log10(self.p_target)
        return 10 ** fsolve(
            func=(
                lambda log_eint: mmt.CstMetalState(
                    self.eos, self.he, self.dens, 10**log_eint
                ).compute(mmt.StateVar.LogPressure)
                - logp
            ),
            x0=np.log10(self.p_target / self.dens / 0.5),
            xtol=self.tol,
        )

    @cached_property
    def state(self) -> mmt.CstMetalState:
        return mmt.CstMetalState(self.eos, self.he, self.dens, self.e_int)

    @cached_property
    def gamma1(self) -> NDArray[np.float64]:
        return self.state.compute(mmt.StateVar.Gamma1)

    @cached_property
    def pressure(self) -> NDArray[np.float64]:
        return 10 ** self.state.compute(mmt.StateVar.LogPressure)


@dataclass(frozen=True)
class Abundances:
    geom: Geometry
    fgong: FgongModel
    metallicity: float
    he_mode: str
    he_frac_if_constant: float

    def with_active_he(self) -> Abundances:
        return Abundances(
            geom=self.geom,
            fgong=self.fgong,
            metallicity=self.metallicity,
            he_mode="active",
            he_frac_if_constant=self.he_frac_if_constant,
        )

    @cached_property
    def he_frac(self) -> NDArray[np.float64]:
        match self.he_mode:
            case "constant":
                return np.full_like(self.geom.r_centers, self.he_frac_if_constant)
            case "active" | "frozen":
                return np.interp(
                    self.geom.r_centers,
                    self.fgong.radius,
                    1.0 - self.metallicity - self.fgong.h_frac,
                )
            case _:
                raise ValueError(f"unknown he_mode={self.he_mode}")

    @property
    def he_constant(self) -> bool:
        return self.he_mode == "constant"

    @property
    def he_scalar(self) -> bool:
        return not self.he_constant

    @property
    def he_active(self) -> bool:
        return self.he_mode == "active"

    def nml_patch(self) -> dict[str, dict[str, object]]:
        patch: dict[str, dict[str, object]] = {}
        patch["abundances"] = dict(
            helium_scalar=1 if self.he_scalar else 0,
            metals_mass_fraction=self.metallicity,
        )
        if self.he_constant:
            patch["abundances"]["helium_mass_fraction"] = self.he_frac_if_constant
        patch["scalars"] = dict(
            nscalars=1 if self.he_scalar else 0,
            nactive_scalars=1 if self.he_active else 0,
            evolve_scalars=self.he_active,
        )
        return patch

    def _diff(
        self,
        label: str,
        prescribed: float,
        actual: NDArray[np.float64],
        console: Console,
    ) -> None:
        departure = np.abs(actual - prescribed)
        imax = np.argmax(departure)
        msg = (
            f"{label}[{imax}] = {actual[imax]:.10f}, "
            f"while prescribed value is {prescribed:.10f}"
        )
        if departure[imax] > 1e-5:
            console.print(Text(f"WARNING: {msg}", style=Style(color="yellow")))
        elif departure[imax] > 1e-10:
            console.print(Text(f"INFO: {msg}", style=Style(dim=True)))

    def report_diff(self, console: Console) -> None:
        metal_frac = np.interp(
            self.geom.r_centers[1:-1],
            self.fgong.radius,
            self.fgong.metal_frac,
        )
        self._diff("metallicity", self.metallicity, metal_frac, console)

        if self.he_constant:
            he_frac = self.with_active_he().he_frac
            self._diff("he_frac", self.he_frac_if_constant, he_frac, console)


@dataclass(frozen=True)
class ProfilesHSE:
    geom: Geometry
    n2_f: NDArray[np.float64]
    he_c: NDArray[np.float64]
    dens_gc_top: np.float64
    press_gc_top: np.float64
    mass_top: np.float64
    eos: mmt.CstMetalEos
    phys_consts: PhysConsts
    eos_tol: float
    n2_tol: float
    report_to: Console | None = None

    @property
    def r_f(self) -> NDArray[np.float64]:
        return self.geom.r_faces

    @property
    def r_c(self) -> NDArray[np.float64]:
        return self.geom.r_centers

    @cached_property
    def _solve(self) -> list[ThermoState]:
        mass_f = self.mass_top
        states = [
            ThermoState(
                he=np.array([self.he_c[-1]]),
                dens=np.array([self.dens_gc_top]),
                p_target=np.array([self.press_gc_top]),
                eos=self.eos,
                tol=self.eos_tol,
            )
        ]
        prog = progress.Progress(
            progress.SpinnerColumn(),
            progress.TextColumn("{task.description}"),
            progress.MofNCompleteColumn(),
            console=self.report_to,
            disable=self.report_to is None,
            transient=True,
        )
        prof_task = prog.add_task("constructing profiles...", total=self.r_f.size)
        prog.start()
        for i_f in range(self.r_f.size - 1, -1, -1):
            g_f = self.phys_consts.gravitational * mass_f / self.r_f[i_f] ** 2
            sp = states[-1]

            # center (i_f - 1) is at index i_f because of gc
            dr = self.r_c[i_f + 1] - self.r_c[i_f]

            he_c = np.array([self.he_c[i_f]])

            def residual(log_dens_c: NDArray[np.float64]) -> NDArray[np.float64]:
                dens_c = 10**log_dens_c
                dens_f = (sp.dens + dens_c) / 2
                dp_dr = -dens_f * g_f

                sn = ThermoState(
                    he=he_c,
                    dens=dens_c,
                    p_target=sp.pressure - dp_dr * dr,
                    eos=self.eos,
                    tol=self.eos_tol,
                )
                drho_dr = (sp.dens - sn.dens) / dr
                press_f = (sp.pressure + sn.pressure) / 2
                gamma1_f = (sn.gamma1 + sp.gamma1) / 2
                dp_dr = (sp.pressure - sn.pressure) / dr

                resid_n2 = self.n2_f[i_f] - g_f * (
                    dp_dr / (gamma1_f * press_f) - drho_dr / dens_f
                )
                return resid_n2

            dens_c = 10 ** fsolve(func=residual, x0=np.log10(sp.dens), xtol=self.n2_tol)
            dens_f = (sp.dens + dens_c) / 2
            dp_dr = -dens_f * g_f

            states.append(
                ThermoState(
                    he=he_c,
                    dens=dens_c,
                    p_target=sp.pressure - dp_dr * dr,
                    eos=self.eos,
                    tol=self.eos_tol,
                )
            )
            prog.advance(prof_task, advance=1)

            dr3 = self.r_f[i_f] ** 3 - self.r_f[i_f - 1] ** 3
            mass_f = mass_f - 4 * np.pi * dens_c * dr3 / 3

        prog.stop()
        return states

    @cached_property
    def music_profs(self) -> MusicProfs:
        density = np.flip([s.dens.item() for s in self._solve])
        e_int = np.flip([s.e_int.item() for s in self._solve])
        return MusicProfs(
            geom=self.geom,
            he_frac=self.he_c,
            density=density,
            e_int=e_int,
            eos=self.eos,
            phys_consts=self.phys_consts,
            mass_top=self.mass_top,
        )


@dataclass(frozen=True)
class MusicProfs:
    geom: Geometry
    he_frac: NDArray[np.float64]
    density: NDArray[np.float64]
    e_int: NDArray[np.float64]
    eos: mmt.CstMetalEos
    phys_consts: PhysConsts
    mass_top: np.float64

    @property
    def r_f(self) -> NDArray[np.float64]:
        return self.geom.r_faces

    @property
    def r_c(self) -> NDArray[np.float64]:
        return self.geom.r_centers

    @cached_property
    def state(self) -> mmt.CstMetalState:
        return mmt.CstMetalState(
            self.eos,
            he_frac=self.he_frac,
            density=self.density,
            energy=self.e_int,
        )

    @cached_property
    def pressure(self) -> NDArray[np.float64]:
        return 10 ** self.state.compute(mmt.StateVar.LogPressure)

    @cached_property
    def temperature(self) -> NDArray[np.float64]:
        return 10 ** self.state.compute(mmt.StateVar.LogTemperature)

    @cached_property
    def xmass(self) -> NDArray[np.float64]:
        """mass coordinate at cell faces"""
        dvol = 4 * np.pi * np.diff(self.r_f**3) / 3
        dm = self.density[1:-1] * dvol
        m_face = np.zeros_like(self.r_f)
        m_face[-1] = self.mass_top
        m_face[:-1] = np.flip(self.mass_top - np.cumsum(np.flip(dm)))
        return m_face

    @cached_property
    def grav(self) -> NDArray[np.float64]:
        """gravity at cell faces"""
        return self.phys_consts.gravitational * self.xmass / self.r_f**2

    @cached_property
    def dlnp_dr(self) -> NDArray[np.float64]:
        press_f = center_with_gc_to_faces(self.pressure)
        return np.diff(self.pressure) / np.diff(self.r_c) / press_f

    @cached_property
    def hp_resol(self) -> NDArray[np.float64]:
        return -1 / (self.dlnp_dr * np.diff(self.r_c))

    @cached_property
    def n2(self) -> NDArray[np.float64]:
        """Brunt-Vaisala frequency at faces"""
        dens_f = center_with_gc_to_faces(self.density)

        gamma_f = center_with_gc_to_faces(self.state.compute(mmt.StateVar.Gamma1))
        dlnrho_dr = np.diff(self.density) / np.diff(self.r_c) / dens_f

        return self.grav * (self.dlnp_dr / gamma_f - dlnrho_dr)

    @cached_property
    def r_env(self) -> float:
        r_env = 0.0
        # points where N2 flips sign and becomes positive downwards
        n2_flips = np.diff(np.sign(self.n2), prepend=self.n2[0]) < 0
        in_search_region = 0.05 * self.geom.r_star < self.r_f
        in_search_region &= self.r_f < 0.9 * self.geom.r_star
        r_candidates = self.r_f[n2_flips & in_search_region]

        for r in r_candidates[::-1]:
            above = self.r_f >= r
            is_conv = self.n2 <= 0.0
            conv_frac_above = len(self.r_f[above & is_conv]) / len(self.r_f[above])
            if conv_frac_above > 0.5:
                r_env = r

        return r_env

    @cached_property
    def r_core(self) -> float:
        r_core = 0.0
        # points where N2 flips sign and becomes positive upwards
        n2_flips = np.diff(np.sign(self.n2), append=self.n2[-1]) > 0
        in_search_region = self.r_f < 0.7 * self.geom.r_star
        r_candidates = self.r_f[n2_flips & in_search_region]

        for r in r_candidates:
            below = self.r_f <= r
            is_conv = self.n2 <= 0.0
            conv_frac_below = len(self.r_f[below & is_conv]) / len(self.r_f[below])
            if conv_frac_below > 0.5:
                r_core = r
        return r_core


@dataclass(frozen=True)
class MusicRunSetup:
    fgong: FgongModel
    music: MusicProfs
    geom: Geometry
    abundances: Abundances

    @cached_property
    def luminosity_f(self) -> NDArray[np.float64]:
        """Luminosity at cell faces, interpolated from fgong."""
        # avoid central point where luminosity is 0
        return np.exp(
            np.interp(
                self.music.r_f,
                self.fgong.radius[1:],
                np.log(self.fgong.luminosity[1:]),
            )
        )

    def write_ic(self, path: Path) -> None:
        header = Header(
            xmcore=self.music.xmass[0],
            time=0.0,
            spherical=True,
            face_loc_1=self.music.r_f,
            face_loc_2=self.geom.theta_faces,
            face_loc_3=self.geom.phi_faces,
        )
        shape = [self.geom.theta_faces.size - 1, self.music.r_f.size - 1]
        if self.geom.phi_faces is not None:
            shape.insert(0, self.geom.phi_faces.size - 1)
        density = np.broadcast_to(self.music.density[1:-1], shape).T
        data = dict(
            rho=density,
            e=np.broadcast_to(self.music.e_int[1:-1], shape).T,
            v_r=np.zeros_like(density),
            v_t=np.zeros_like(density),
        )
        if self.geom.nmom >= 3:
            data["v_p"] = np.zeros_like(density)
        if self.abundances.he_scalar:
            data["Scalar1"] = np.broadcast_to(self.music.he_frac[1:-1], shape).T
        MusicNewFormatDumpFile(path).write(header, data)

    def write_prof1d(self, path: Path) -> None:
        df_header = pd.DataFrame(
            dict(
                L_inner=self.luminosity_f[0],
                L_outer=self.luminosity_f[-1],
                L_surf=self.fgong.luminosity[-1],
                rad_surf=self.fgong.r_star,
                rcore=self.music.r_core,
                renv=self.music.r_env,
            ),
            index=[0],
        )
        df_data = pd.DataFrame(
            dict(
                r_face=self.music.r_f,
                gravity=self.music.grav,
                bv_freq2=self.music.n2,
                luminosity=self.luminosity_f,
                r_center=self.music.r_c[1:],
                density=self.music.density[1:],
                e_int_spec=self.music.e_int[1:],
                he_frac=self.music.he_frac[1:],
                pressure=self.music.pressure[1:],
                temperature=self.music.temperature[1:],
                nuclear_heating=np.interp(
                    self.music.r_c[1:],
                    self.fgong.radius,
                    self.fgong.e_nuclear,
                ),
            ),
            index=range(1, self.music.r_f.size + 1),
        )
        with path.open("w") as p1df:
            df_header.to_string(
                buf=p1df,
                index=False,
                float_format=lambda x: f"{x:.15e}",
            )
            p1df.write("\ni")
            df_data.to_string(
                buf=p1df,
                float_format=lambda x: f"{x:.15e}",
            )
            p1df.write("\n")

    def update_nml(self, run_path: RunPath, nml_in: Path) -> None:
        nml: dict[str, dict[str, object]] = {}
        nml["dims"] = dict(
            ndim=self.geom.ndim,
            nmom=self.geom.nmom,
        )

        nml["io"] = dict(
            input=str(run_path.ic_relative),
        )

        nml["boundaryconditions"] = dict(
            energy_flux_type="luminosity",
            inner_flux=self.luminosity_f[0],
            outer_flux=self.luminosity_f[-1],
        )

        nml["physics"] = dict(
            constants_revision=self.music.phys_consts.label,
            thermal_diffusion_type="scaled_radiative",
            thermal_diffusion_value=1.0,
            specific_internal_energy_term_profile1d_filename=str(
                run_path.prof1d_relative
            ),
            specific_internal_energy_term_profile1d_column="nuclear_heating",
        )

        nml["gravity"] = dict(
            gravity_type="self_gravity_1d",
        )

        nml["microphysics"] = dict(
            eos="mesa",
            opacities="mesa",
        )

        nml["eos_mesa"] = dict()
        nml["opacity_mesa"] = dict()

        try:
            nml_read = f90nml.read(nml_in)
        except FileNotFoundError:
            nml_read = f90nml.Namelist()
        nml_read.patch(nml)
        nml_read.patch(self.abundances.nml_patch())
        nml_read.write(run_path.nml, force=True)

    def _log_interp(self, arr_fg: NDArray[np.floating]) -> NDArray[np.floating]:
        """log-interpolate fgong profile on MUSIC centers (with gc)"""
        return np.exp(np.interp(self.geom.r_centers, self.fgong.radius, np.log(arr_fg)))

    def _vol_avg(self, arr_c: NDArray[np.floating]) -> np.floating:
        """volume average of quantity known at MUSIC centers (without gc)"""
        dr3 = np.diff(self.geom.r_faces**3)
        vol = np.sum(dr3)
        return np.sum(arr_c * dr3) / vol

    def diagnostics(self, console: Console) -> None:
        table = Table(
            title="(fgong(interp) - music) / fgong(interp)",
            box=box.SIMPLE,
        )
        table.add_column()
        table.add_column("L2")
        table.add_column("Linf")

        def report_l2_linf_diff(
            arr1_fg: NDArray[np.floating], arr2_gc: NDArray, label: str
        ) -> None:
            arr1_gc = self._log_interp(arr1_fg)
            arr = (arr1_gc - arr2_gc) / arr1_gc
            arr = arr[1:-1]  # rm ghostcells
            l2 = np.sqrt(self._vol_avg(arr**2))
            linf = np.amax(np.abs(arr))
            table.add_row(label, f"{l2:.5e}", f"{linf:.5e}")

        report_l2_linf_diff(self.fgong.density, self.music.density, label="density")
        report_l2_linf_diff(self.fgong.pressure, self.music.pressure, label="pressure")
        report_l2_linf_diff(
            self.fgong.temperature, self.music.temperature, label="temperature"
        )
        console.print()
        console.print(table)

    def comparison_plots(self, path: Path) -> None:
        mprofs = self.music
        fgong = self.fgong

        fig, axes = plt.subplots(ncols=3, nrows=3, figsize=(15, 12), sharex=True)

        for ax in axes.flat:
            if mprofs.r_env > 0:
                ax.axvline(mprofs.r_env, color="k", linewidth=0.5)
            if mprofs.r_core > 0:
                ax.axvline(mprofs.r_core, color="k", linewidth=0.5)

        axes[0, 0].semilogy(fgong.radius, fgong.density, label="fgong")
        axes[0, 0].plot(mprofs.r_c, mprofs.density, label="music")
        axes[0, 0].legend()
        axes[0, 0].set_ylabel("density")

        axes[0, 1].semilogy(fgong.radius, fgong.pressure, label="fgong")
        axes[0, 1].plot(mprofs.r_c, mprofs.pressure, label="music")
        axes[0, 1].set_ylabel("pressure")

        axes[0, 2].plot(fgong.radius, fgong.temperature, label="fgong")
        axes[0, 2].plot(mprofs.r_c, mprofs.temperature, label="music")
        axes[0, 2].set_ylabel("temperature")

        axes[1, 0].plot(fgong.radius, fgong.metal_frac, label="fgong")
        axes[1, 0].hlines(
            xmin=mprofs.r_f[0],
            xmax=mprofs.r_f[-1],
            y=self.abundances.metallicity,
            color="tab:orange",
            label="music",
        )
        axes[1, 0].set_ylabel("metallicity")

        axes[1, 1].plot(
            fgong.radius,
            1 - fgong.metal_frac - fgong.h_frac,
            label="fgong",
        )
        axes[1, 1].plot(mprofs.r_c, mprofs.he_frac, label="music")
        axes[1, 1].set_ylabel("Helium fraction")

        r_mid_fgong = (fgong.radius[1:] + fgong.radius[:-1]) / 2
        dp_dr_fgong = np.diff(fgong.pressure) / np.diff(fgong.radius)
        dp_dr = np.diff(mprofs.pressure) / np.diff(mprofs.r_c)
        axes[1, 2].semilogy(r_mid_fgong, -dp_dr_fgong, label="fgong")
        axes[1, 2].semilogy(mprofs.r_f, -dp_dr, label="music")
        axes[1, 2].set_ylabel("$-dp/dr$ at faces")

        axes[2, 0].plot(fgong.radius, fgong.bv_freq2, label="fgong")
        axes[2, 0].plot(mprofs.r_f, mprofs.n2, label="music")
        axes[2, 0].set_ylabel("$N^2$")
        axes[2, 0].set_yscale("asinh", linear_width=1e-12)

        dens_f = center_with_gc_to_faces(mprofs.density)
        residual_hse = 1 + dp_dr / (dens_f * mprofs.grav)
        axes[2, 1].plot(
            mprofs.r_f, residual_hse, label="music", lw=0.3, color="tab:orange"
        )
        axes[2, 1].set_ylabel(r"HSE residual $1 + dp/(\rho g dr)$ at faces")

        axes[2, 2].plot(mprofs.r_f, mprofs.hp_resol, label="music", color="tab:orange")
        axes[2, 2].set_ylabel(r"$H_p / \delta r$")

        for ax in axes[-1, :]:
            ax.set_xlabel("radius")

        fig.tight_layout()
        fig.savefig(path)


@dataclass(frozen=True)
class RunPath:
    root: Path
    ic_relative: Path
    nml_relative: Path
    prof1d_relative: Path

    @cached_property
    def prof1d(self) -> Path:
        return self.root / self.prof1d_relative

    @cached_property
    def ic(self) -> Path:
        return self.root / self.ic_relative

    @cached_property
    def nml(self) -> Path:
        return self.root / self.nml_relative


def main(cli_conf: CliConfig) -> None:
    console = Console()

    conf = Config.default_()
    conf_file = cli_conf.ic_stellar.config
    if conf_file.is_file():
        conf.update_from_file_(cli_conf.ic_stellar.config)
    else:
        console.print(f"creating config file {conf_file}")
        conf.to_file_(conf_file, exist_ok=False)
        return

    fgong = FgongModel(
        conf.sources.fgong,
        phys_consts=REVISIONS[conf.physics.constants_revision],
    )

    geom = Geometry.from_conf(conf.grid, conf.physics.nmom, fgong.r_star)

    abundances = Abundances(
        geom=geom,
        fgong=fgong,
        metallicity=conf.mesa_eos.metallicity,
        he_mode=conf.mesa_eos.he_mode,
        he_frac_if_constant=conf.mesa_eos.he_frac,
    )

    abundances.report_diff(console)

    profs = ProfilesHSE(
        geom=geom,
        n2_f=np.interp(geom.r_faces, fgong.radius, fgong.bv_freq2),
        he_c=abundances.he_frac,
        dens_gc_top=np.exp(
            np.interp(geom.r_centers[-1], fgong.radius, np.log(fgong.density)).item()
        ),
        press_gc_top=np.exp(
            np.interp(geom.r_centers[-1], fgong.radius, np.log(fgong.pressure)).item()
        ),
        mass_top=np.interp(geom.r_faces[-1] ** 3, fgong.radius**3, fgong.xmass).item(),
        eos=mmt.CstMetalEos(metallicity=abundances.metallicity),
        phys_consts=fgong.phys_consts,
        eos_tol=conf.inversion.eos_tol,
        n2_tol=conf.inversion.n2_tol,
        report_to=console,
    )
    mprofs = profs.music_profs

    run_path = RunPath(
        root=conf.output.music_run_dir,
        ic_relative=conf.output.ic,
        nml_relative=conf.output.nml,
        prof1d_relative=Path("profile1d_scalars.dat"),
    )
    run_path.root.mkdir(parents=True, exist_ok=True)
    run_setup = MusicRunSetup(
        fgong=fgong,
        music=mprofs,
        geom=geom,
        abundances=abundances,
    )

    with console.status("drawing plots..."):
        run_setup.comparison_plots(run_path.root / "fgong_vs_music.pdf")
    run_setup.diagnostics(console)

    run_setup.write_ic(path=run_path.ic)
    run_setup.write_prof1d(path=run_path.prof1d)
    run_setup.update_nml(run_path=run_path, nml_in=conf.sources.nml_template)
