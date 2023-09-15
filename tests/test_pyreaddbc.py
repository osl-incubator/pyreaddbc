import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import pandas as pd
import pytest
from dbfread import DBF

from pyreaddbc import dbc2dbf

path_root = Path(__file__).resolve().parent.parent
data_files = path_root / "tests/data"


def read_dbc(filename, encoding="utf-8", raw=False):
    """
    Opens a DBC file and returns its contents as a pandas DataFrame.

    Parameters:
        filename (str):
            The name of the .dbc file.
        encoding (str, optional):
            The encoding of the data (default is "utf-8").
        raw (bool, optional):
            If True, skips type conversion to avoid
                type conversion errors (default is False).

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the DBC file.
    """

    if isinstance(filename, str):
        filename = filename.encode()
    with NamedTemporaryFile(delete=False) as tf:
        dbc2dbf(filename, tf.name.encode())
        try:
            dbf = DBF(tf.name, encoding=encoding, raw=raw)
            df = pd.DataFrame(list(dbf))
        except ValueError:
            dbf = DBF(tf.name, encoding=encoding, raw=not raw)
            df = pd.DataFrame(list(dbf))
    os.unlink(tf.name)
    return df


def read_dbc_dbf(filename: str) -> pd.DataFrame:
    """
    Read a DBC or DBF file and return its contents as a pandas DataFrame.

    Parameters:
        filename (str): The name of the file to read.

    Returns:
        pd.DataFrame: A DataFrame containing the data from the file.
    """
    if filename.endswith(("dbc", "DBC")):
        df = read_dbc(filename, encoding="iso-8859-1")
    elif filename.endswith(("DBF", "dbf")):
        dbf = DBF(filename, encoding="iso-8859-1")
        df = pd.DataFrame(list(dbf))
    return df


# DATASUS Databases
db_tests = [
    "ZIKABR21",
    "STPI2206",
    "sids",
]


@pytest.mark.parametrize("db_test", db_tests)
def test_read_dbc(db_test):
    dbc_file = str(data_files / f"{db_test}.dbc")
    df = read_dbc(dbc_file)
    assert_dataframe_valid(df)


@pytest.mark.parametrize("db_test", db_tests)
def test_dbc2dbf(db_test):
    dbc_file = str(data_files / f"{db_test}.dbc")
    temp_dbf_file = str(data_files / f"{db_test}.dbf")
    dbc2dbf(dbc_file, temp_dbf_file)
    assert os.path.isfile(temp_dbf_file)
    df = read_dbc_dbf(temp_dbf_file)
    assert_dataframe_valid(df)


@pytest.mark.parametrize("db_test", db_tests)
def test_dbc_file_header(db_test):
    dbc_file = data_files / f"{db_test}.dbc"
    with open(dbc_file, 'rb') as f:
        header = f.read(32)
        valid_headers = [
            (b'\x03{\x08\x07', b'\xe1\x04\x9c\x00'),
            (b'\x03z\x07\x0c', b'!\x1a\xf3\x01'),
            (b'\x03g\x06\x11', b'\xe1\x01\xa8\x00'),
        ]
        is_valid = any(
            len(header) == 32 and header[0:4] == h[0] and header[8:12] == h[1]
            for h in valid_headers
        )
        assert is_valid, f"{dbc_file} is not a valid DBC file."


def assert_dataframe_valid(df):
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert df.shape[0] > 0
    assert df.shape[1] > 0
