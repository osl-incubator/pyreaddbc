u"""
Created on 16/08/16
by fccoelho
license: GPL V3 or Later
"""
import os

from cffi import FFI
from pathlib import Path

ffibuilder = FFI()

PROJECT_PATH = Path(__file__).parent.parent
PACKAGE_ABS_PATH = Path(__file__).parent
PACKAGE_REL_PATH = PACKAGE_ABS_PATH.relative_to(PROJECT_PATH)

with open(PACKAGE_ABS_PATH / "c-src" / "dbc2dbf.c", "r") as f:
    ffibuilder.set_source(
        module_name="pyreaddbc._readdbc",
        source=f.read(),
        source_extension=".c",
        libraries=["c"],
        sources=[str(PACKAGE_REL_PATH / "c-src" / "blast.c")],
        include_dirs=[str(PACKAGE_REL_PATH / "c-src")],
    )
ffibuilder.cdef(
    """
    static unsigned inf(void *how, unsigned char **buf);
    static int outf(void *how, unsigned char *buf, unsigned len);
    void dbc2dbf(char** input_file, char** output_file);
    """
)

with open(PACKAGE_ABS_PATH / "c-src" / "blast.h") as f:
    ffibuilder.cdef(f.read(), override=True)


if __name__ == "__main__":
    ffibuilder.compile(
        # tmpdir=str(),
        target="_readdbc.so",
        verbose=True,
        debug=True,
    )
