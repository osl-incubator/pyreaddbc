u"""
Created on 16/08/16
by fccoelho
license: GPL V3 or Later
"""
import os

from cffi import FFI
import shutil
from pathlib import Path

ffibuilder = FFI()


pyreaddbc_PATH = os.path.dirname(__file__)
ROOT_PATH = os.path.dirname(pyreaddbc_PATH)

with open(os.path.join(pyreaddbc_PATH, "c-src/dbc2dbf.c"), "r") as f:
    ffibuilder.set_source(
        "_readdbc",
        f.read(),
        libraries=["c"],
        sources=[os.path.join(pyreaddbc_PATH, "c-src/blast.c")],
        include_dirs=[os.path.join(pyreaddbc_PATH, "c-src/")],
    )
ffibuilder.cdef(
    """
    static unsigned inf(void *how, unsigned char **buf);
    static int outf(void *how, unsigned char *buf, unsigned len);
    void dbc2dbf(char** input_file, char** output_file);
    """
)

with open(os.path.join(pyreaddbc_PATH, "c-src/blast.h")) as f:
    ffibuilder.cdef(f.read(), override=True)


if __name__ == "__main__":
    ffibuilder.compile(
        tmpdir=".",
        target=f"{pyreaddbc_PATH}/_readdbc.so",
        verbose=True,
        debug=True,
    )
    shutil.move(Path(ROOT_PATH) / "_readdbc*.so", pyreaddbc_PATH)
