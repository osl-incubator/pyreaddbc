"""
Created on 16/08/16
by fccoelho
license: GPL V3 or Later
"""
import os

try:
    from pyreaddbc._readdbc import ffi, lib
except (ImportError, ModuleNotFoundError):
    from ._readdbc import ffi, lib


def dbc2dbf(infile, outfile):
    """
    Converts a DBC file to a DBF database saving it to `outfile`.
    :param infile: .dbc file name
    :param outfile: name of the .dbf file to be created.
    """
    if isinstance(infile, str):
        infile = infile.encode()
    if isinstance(outfile, str):
        outfile = outfile.encode()
    p = ffi.new("char[]", os.path.abspath(infile))
    q = ffi.new("char[]", os.path.abspath(outfile))

    lib.dbc2dbf([p], [q])
