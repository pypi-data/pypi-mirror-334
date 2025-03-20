from __future__ import annotations

import typing
from pathlib import Path

import numpy as np
from scipy.io import FortranFile

if typing.TYPE_CHECKING:
    from typing import Any, Mapping, MutableMapping, Sequence

    from numpy.typing import NDArray


class _MusicFormat1Block:
    """See io.90:idvp_write()"""

    def __init__(self, ndim: int):
        assert ndim in {2, 3}
        self.ndim = ndim

    @property
    def header_fields(self) -> Mapping[str, np.dtype]:
        return {
            "gms": np.dtype("float64"),
            "xmcore": np.dtype("float64"),
            "model": np.dtype("int32"),
            "dtn": np.dtype("float64"),
            "time": np.dtype("float64"),
            "nfaces": np.dtype(("int32", (self.ndim,))),
        }

    def grid_fields(self, nfaces: NDArray[np.integer]) -> Mapping[str, np.dtype]:
        return {
            f"face_loc_{i}": np.dtype(("float64", (n,)))
            for i, n in enumerate(nfaces, 1)
        }

    def datablock_dtype(self, nfaces: NDArray[np.integer]) -> np.dtype:
        nvars = len(self.data_vars)
        shape = tuple(nfaces) + (nvars,)
        return np.dtype(("float64", shape))

    @property
    def data_vars(self) -> Sequence[str]:
        return ["density", "e_int_spec"] + [f"vel_{i + 1}" for i in range(self.ndim)]

    def nbytes(self, nfaces: NDArray[np.integer]) -> int:
        def nbytes(fields: Mapping[str, np.dtype]) -> int:
            return sum(dtype.itemsize for dtype in fields.values())

        marker = np.dtype("int32")  # dtype of Fortran record marker
        return (
            3 * marker.itemsize * 2  # 3 fields, 2 markers (beg + end) per field
            + nbytes(self.header_fields)
            + nbytes(self.grid_fields(nfaces))
            + self.datablock_dtype(nfaces).itemsize
        )


class MusicFormat1DumpFile:
    def __init__(self, file_name: Path, ndim: int):
        self.file_name = file_name
        self.ndim = ndim

        self._block = _MusicFormat1Block(self.ndim)
        self._is_open = False
        self._file = open(file_name, "rb")
        self._fortran_file = FortranFile(self._file, mode="r")
        self._is_open = True

        # Read nfaces from first header, precompute block size, reset file cursor
        self._nfaces = self._read_fields(self._block.header_fields)["nfaces"]
        self._block_nbytes = self._block.nbytes(self._nfaces)
        self._file.seek(0)

        # Compute number of dumps stored in file
        file_size = Path(self.file_name).stat().st_size
        assert file_size % self._block_nbytes == 0
        self.num_dumps = file_size // self._block_nbytes

    def __enter__(self) -> MusicFormat1DumpFile:
        assert self._is_open
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()

    def close(self) -> None:
        if self._is_open:
            self._fortran_file.close()
            self._file.close()
            self._is_open = False

    def _read_fields(
        self, fields: Mapping[str, np.dtype]
    ) -> MutableMapping[str, NDArray]:
        names, dtypes = fields.keys(), fields.values()
        data = [np.squeeze(x) for x in self._fortran_file.read_record(*dtypes)]
        return dict(zip(names, data))

    def _seek_to_dump(self, idump: int) -> None:
        if idump < 0:
            idump += self.num_dumps
        assert 0 <= idump < self.num_dumps
        self._file.seek(idump * self._block_nbytes)

    def read(self, idump: int = -1) -> tuple:
        self._seek_to_dump(idump)
        header = self._read_fields(self._block.header_fields)
        header.update(self._read_fields(self._block.grid_fields(self._nfaces)))

        data_vars = self._block.data_vars
        data_block = self._fortran_file.read_record(
            self._block.datablock_dtype(self._nfaces)
        )
        # Slice data block into variables
        data = {
            var: data_block.take(i, axis=self.ndim) for i, var in enumerate(data_vars)
        }
        return header, data
