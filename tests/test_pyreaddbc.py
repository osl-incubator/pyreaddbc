import os
from pathlib import Path

import chardet
import pandas as pd
import pytest

from pyreaddbc import dbc2dbf, read_dbc, read_dbc_dbf

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
    assert len(df.columns) > 0
    assert len(df) > 0
    assert df.shape[0] > 0
    assert df.shape[1] > 0
