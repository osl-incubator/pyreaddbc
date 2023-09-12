import gzip
import os
from pathlib import Path

import chardet
import pandas as pd
import pytest

from pyreaddbc import dbc2dbf, dbf_to_csvgz, read_dbc, read_dbc_dbf

path_root = Path(__file__).resolve().parent.parent
data_files = path_root / "tests/data"


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
def test_read_dbc_dbf(db_test):
    dbc_file = str(data_files / f"{db_test}.dbc")
    df = read_dbc_dbf(dbc_file)
    assert_dataframe_valid(df)


@pytest.mark.parametrize("db_test", db_tests)
def test_dbf_to_csvgz(db_test):
    temp_dbf_file = str(data_files / f"{db_test}.dbf")
    temp_csvgz_file = str(data_files / f"{db_test}.csv.gz")
    dbf_to_csvgz(temp_dbf_file, encoding='iso-8859-1')
    assert os.path.isfile(temp_csvgz_file)
    with gzip.open(temp_csvgz_file, "rt") as gzfile:
        df = pd.read_csv(gzfile)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) > 2
    assert len(df) > 0


@pytest.mark.parametrize("db_test", db_tests)
@pytest.mark.skipif
def test_encoding(db_test):
    dbc_file = str(data_files / f"{db_test}.dbc")
    common_encodings = [
        'utf-8',
        'iso-8859-1',
        'cp1252',
        'Windows-1252',
    ]  # Add more if needed

    detected_encoding = chardet.detect(open(dbc_file, 'rb').read())['encoding']
    assert detected_encoding in common_encodings


@pytest.mark.parametrize("db_test", db_tests)
def test_dbc_file_header(db_test):
    dbc_file = str(data_files / f"{db_test}.dbc")
    with open(dbc_file, 'rb') as dbc_file:
        # Read the first 32 bytes of the file
        header = dbc_file.read(32)

        # Check if the header is valid
        if (
            len(header) != 32
            or header[0:4] != b'VJDB'
            or header[8:12] != b'\x01\x00\x00\x00'
        ):
            print(f"Error: {dbc_file} is not a valid DBC file.")
            return False

    print(f"{dbc_file} is a valid DBC file.")
    return True


def assert_dataframe_valid(df):
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df.columns) > 0
    assert len(df) > 0
    assert df.shape[0] > 0
    assert df.shape[1] > 0
