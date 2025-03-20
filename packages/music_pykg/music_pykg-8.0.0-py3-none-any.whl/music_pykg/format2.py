from __future__ import annotations

import os
from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from types import MappingProxyType
from typing import (
    BinaryIO,
    Callable,
    Generic,
    Iterator,
    Literal,
    Mapping,
    Sequence,
    TypeVar,
)

import numpy as np
from numpy.typing import NDArray

T = TypeVar("T", np.int32, np.float64)

_MUSIC_LOG_HEADER = "MUSIC Log File version 1.2"


@dataclass(frozen=True)
class LogFileArrayRecord(Generic[T]):
    log_file: MusicLogReader
    name: str
    order: Literal["C"] | Literal["F"]
    dims: NDArray[np.int32]
    arr_pos: int
    dtype: type[T]
    squeeze: bool = True

    @cached_property
    def arr_size(self) -> int:
        return np.prod(self.dims).item()

    @cached_property
    def arr_byte_size(self) -> int:
        return np.dtype(self.dtype).itemsize * self.arr_size

    def read(self) -> NDArray[T]:
        self.log_file.fd.seek(self.arr_pos)
        array = self.log_file._rawarr(self.dtype, self.arr_size)
        array = array.reshape(self.dims, order=self.order)
        if self.squeeze:
            array = array.squeeze()
        return array


@dataclass(frozen=True)
class MusicLogReader:
    fd: BinaryIO

    def _rawarr(self, dtype: type[T], count: int) -> NDArray[T]:
        return np.fromfile(self.fd, dtype=dtype, count=count)

    def _get_str(self) -> str | None:
        try:
            length = self._rawarr(np.int32, 1)[0].item()
        except IndexError:
            return None
        str_bytes = self.fd.read(length)
        return str_bytes.decode(encoding="ascii")

    def _str(self) -> str:
        length = self._rawarr(np.int32, 1)[0].item()
        name_bytes = self.fd.read(length)
        return name_bytes.decode(encoding="ascii")

    def _byte(self) -> int:
        """Read one byte."""
        return self.fd.read(1)[0]

    @cached_property
    def _content_start(self) -> int:
        self.fd.seek(0)
        if self._str() != _MUSIC_LOG_HEADER:
            raise RuntimeError("Invalid header in MusicLogFile")
        return self.fd.tell()

    def seek_content_start(self) -> None:
        self.fd.seek(self._content_start)

    def read_named_scalar(self, name: str, dtype: type[T]) -> T:
        name_tag = self._str()
        if name != name_tag:
            raise ValueError(
                f"invalid log item name, expected '{name}', got '{name_tag}'"
            )
        _ = self._byte()  # FIXME: check type flag
        scalar = self._rawarr(dtype, 1)
        return scalar[0]

    def get_array_record(
        self,
        dtype: type[T],
        squeeze: bool = True,
    ) -> LogFileArrayRecord | None:
        if (name := self._get_str()) is None:
            return None
        _ = self._byte()  # FIXME: check type flag
        order_flag = self._byte()
        if order_flag not in (0, 1):
            raise RuntimeError(f"Order flag has unexpected value {order_flag}")
        dims = self._rawarr(np.int32, 3)
        record = LogFileArrayRecord(
            log_file=self,
            name=name,
            order="C" if order_flag == 0 else "F",
            dims=dims,
            arr_pos=self.fd.tell(),
            dtype=dtype,
            squeeze=squeeze,
        )
        self.fd.seek(record.arr_byte_size, os.SEEK_CUR)
        return record

    def read_named_array(
        self, name: str, dtype: type[T], squeeze: bool = True
    ) -> NDArray[T]:
        record = self.get_array_record(dtype, squeeze)
        if record is None:
            raise RuntimeError("Reached EOF")
        if name != record.name:
            raise ValueError(
                f"invalid log item name, expected '{name}', got '{record.name}'"
            )
        return record.read()


@dataclass(frozen=True)
class MusicLogFile:
    path: Path

    @contextmanager
    def reader(self) -> Iterator[MusicLogReader]:
        with self.path.open(mode="rb") as fd:
            yield MusicLogReader(fd=fd)

    @contextmanager
    def writer(self, insert_header: bool) -> Iterator[MusicLogWriter]:
        with self.path.open(mode="wb") as fd:
            writer = MusicLogWriter(fd=fd)
            if insert_header:
                writer.write_header()
            yield writer


@dataclass(frozen=True)
class Header:
    xmcore: float
    time: float
    spherical: bool
    face_loc_1: NDArray[np.float64]
    face_loc_2: NDArray[np.float64]
    face_loc_3: NDArray[np.float64] | None = None
    model: int = 0
    dtn: float = 0.0
    num_ghost: int = 0

    @cached_property
    def nfaces(self) -> tuple[int, int, int]:
        return (
            self.face_loc_1.size,
            self.face_loc_2.size,
            2 if self.face_loc_3 is None else self.face_loc_3.size,
        )


class MusicNewFormatDumpFile:
    """See readwrite_new_format.90:read_new_model_helium{2d,3d}"""

    def __init__(
        self,
        file_name: str | os.PathLike,
        keep_field: Callable[[str], bool] = lambda s: True,
    ):
        self.file_name = Path(file_name)
        self.keep_field = keep_field

    def _read_header(self, f: MusicLogReader) -> Header:
        f.seek_content_start()
        xmcore = f.read_named_scalar("xmcore", np.float64)
        model = f.read_named_scalar("model", np.int32)
        dtn = f.read_named_scalar("dtn", np.float64)
        time = f.read_named_scalar("time", np.float64)
        nfaces = f.read_named_array("dims", np.int32)
        num_ghost = f.read_named_scalar("num_ghost", np.int32)
        geometry = f.read_named_scalar("geometry", np.int32)

        if f.read_named_scalar("eos", np.int32) == 0:
            f.read_named_scalar("gamma", np.float64)
        f.read_named_scalar("ikap", np.int32)
        f.read_named_scalar("Y", np.float64)
        f.read_named_scalar("Z", np.float64)

        return Header(
            xmcore=xmcore.item(),
            model=model.item(),
            dtn=dtn.item(),
            time=time.item(),
            num_ghost=num_ghost.item(),
            spherical=bool(geometry),
            face_loc_1=f.read_named_array("r", np.float64),
            face_loc_2=f.read_named_array("theta", np.float64),
            face_loc_3=f.read_named_array("phi", np.float64) if nfaces[2] > 2 else None,
        )

    def _read_header_and_toc(
        self, f: MusicLogReader
    ) -> tuple[Header, Mapping[str, LogFileArrayRecord[np.float64]]]:
        header = self._read_header(f)

        def gen_toc() -> Iterator[LogFileArrayRecord]:
            seen: set[str] = set()
            while (toc_entry := f.get_array_record(np.float64)) is not None:
                assert toc_entry.name not in seen, (
                    "Duplicate entries for field '{toc_entry.name}' in file '{self.file_name}'"
                )
                seen.add(toc_entry.name)
                if self.keep_field(toc_entry.name):
                    yield toc_entry

        toc = {toc_entry.name: toc_entry for toc_entry in gen_toc()}
        return header, MappingProxyType(toc)

    def read(self) -> tuple[Header, Mapping[str, NDArray[np.float64]]]:
        with MusicLogFile(self.file_name).reader() as reader:
            header, toc = self._read_header_and_toc(reader)
            data = {name: toc_entry.read() for name, toc_entry in toc.items()}
        return header, MappingProxyType(data)

    def write(self, header: Header, data: Mapping[str, NDArray[np.float64]]) -> None:
        with MusicLogFile(self.file_name).writer(insert_header=True) as writer:
            # Header data
            writer.write_f64("xmcore", header.xmcore)
            writer.write_i32("model", header.model)
            writer.write_f64("dtn", header.dtn)
            writer.write_f64("time", header.time)
            writer.write_arr1d_i32("dims", np.array(header.nfaces, dtype=np.int32))
            writer.write_i32("num_ghost", header.num_ghost)
            writer.write_i32("geometry", int(header.spherical))
            writer.write_i32("eos", -1)
            writer.write_i32("ikap", -1)
            writer.write_f64("Y", -1.0)
            writer.write_f64("Z", -1.0)

            # Grid
            writer.write_arr1d_f64("r", header.face_loc_1)
            writer.write_arr1d_f64("theta", header.face_loc_2)
            if header.face_loc_3 is not None:
                writer.write_arr1d_f64("phi", header.face_loc_3)

            # Variables
            writer.write_arr3d_f64("rho", data["rho"])
            writer.write_arr3d_f64("e", data["e"])
            writer.write_arr3d_f64("v_r", data["v_r"])
            writer.write_arr3d_f64("v_t", data["v_t"])
            if (v_p := data.get("v_p")) is not None:
                writer.write_arr3d_f64("v_p", v_p)

            if "b_r" in data:
                writer.write_arr3d_f64("b_r", data["b_r"])
                writer.write_arr3d_f64("b_t", data["b_t"])
                writer.write_arr3d_f64("b_p", data["b_p"])

            # Scalars
            i = 1
            while (scalar_i := data.get(name := f"Scalar{i}")) is not None:
                writer.write_arr3d_f64(name, scalar_i)
                i += 1

    def read_header(self) -> Header:
        with MusicLogFile(self.file_name).reader() as reader:
            return self._read_header(reader)

    @cached_property
    def field_names(self) -> Sequence[str]:
        with MusicLogFile(self.file_name).reader() as reader:
            _, toc = self._read_header_and_toc(reader)
        return list(toc.keys())

    @cached_property
    def num_space_dims(self) -> int:
        return 2 if self.read_header().face_loc_3 is None else 3

    @cached_property
    def num_velocities(self) -> int:
        fields = set(self.field_names)
        return sum(vname in fields for vname in ["v_r", "v_t", "v_p"])

    @cached_property
    def num_scalars(self) -> int:
        fields = set(self.field_names)
        i = 1
        while f"Scalar{i}" in fields:
            i += 1
        return i - 1

    def keeping_only(self, keep: Callable[[str], bool]) -> MusicNewFormatDumpFile:
        return MusicNewFormatDumpFile(
            self.file_name,
            keep_field=lambda field: self.keep_field(field) and keep(field),
        )


@dataclass(frozen=True)
class MusicLogWriter:
    fd: BinaryIO

    def _rawarr(self, arr: NDArray) -> None:
        self.fd.write(arr.tobytes(order="F"))

    def _rawbytes(self, b: Sequence[int]) -> None:
        self._rawarr(np.array(b, dtype="byte"))

    def write_header(self) -> None:
        self._str(_MUSIC_LOG_HEADER)

    def _str(self, name: str) -> None:
        self.fd.write(np.array(len(name), dtype="int32").tobytes())
        self.fd.write(name.encode("ascii"))

    def write_f64(self, name: str, x: float) -> None:
        x_arr = np.array(x, dtype="float64")
        assert x_arr.size == 1
        self._str(name)
        self._rawbytes([2])
        self._rawarr(x_arr)

    def write_i32(self, name: str, x: int) -> None:
        x_arr = np.array(x, dtype="int32")
        assert x_arr.size == 1
        self._str(name)
        self._rawbytes([0])
        self._rawarr(x_arr)

    def write_arr1d_i32(self, name: str, arr: NDArray[np.integer]) -> None:
        self._str(name)
        self._rawbytes([4, 0])
        self._rawarr(np.array([len(arr), 1, 1], dtype="int32"))
        self._rawarr(arr.astype(np.int32))

    def write_arr1d_f64(self, name: str, arr: NDArray[np.floating]) -> None:
        self._str(name)
        self._rawbytes([6, 0])
        self._rawarr(np.array([len(arr), 1, 1], dtype="int32"))
        self._rawarr(arr.astype("float64"))

    def write_arr3d_f64(self, name: str, cube: NDArray[np.floating]) -> None:
        if cube.ndim not in (2, 3):
            raise RuntimeError(
                f"Attempting to write cube with ndim {cube.ndim}, expected 2 or 3"
            )
        cube = np.atleast_3d(cube.astype(np.float64))
        self._str(name)
        self._rawbytes([6, 1])
        self._rawarr(np.array(cube.shape, dtype=np.int32))
        self._rawarr(cube)
