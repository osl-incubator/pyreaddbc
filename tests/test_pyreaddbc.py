import gzip
import os
import unittest
from pathlib import Path

import chardet
import pandas as pd
import pytest

from pyreaddbc import dbc2dbf, dbf_to_csvgz, read_dbc, read_dbc_dbf

path_root = Path(__file__).resolve().parent.parent
data_files = path_root / "tests/data"
dbc_file = str(data_files / "STPI2206.dbc")
temp_dbf_file = str(data_files / "STPI2206.dbf")

dbc_files = [
    "ZIKABR16.dbc",
    "STPI2206.dbc",
    "sids.dbc",
]


class TestDBCChecks(unittest.TestCase):
    def test_read_dbc(self):
        df = read_dbc(dbc_file)
        self.assertDataFrameValid(df)

    def test_dbc2dbf(self):
        dbc2dbf(str(dbc_file), temp_dbf_file)
        self.assertTrue(os.path.isfile(temp_dbf_file))
        df = read_dbc_dbf(temp_dbf_file)
        self.assertDataFrameValid(df)

    def test_read_dbc_dbf(self):
        df = read_dbc_dbf(dbc_file)
        self.assertDataFrameValid(df)

    def test_dbf_to_csvgz(self):
        temp_csvgz_file = str(data_files / "STPI2206.csv.gz")
        dbf_to_csvgz(temp_dbf_file, encoding='iso-8859-1')
        self.assertTrue(os.path.isfile(temp_csvgz_file))
        with gzip.open(temp_csvgz_file, "rt") as gzfile:
            df = pd.read_csv(gzfile)
        assert isinstance(df, pd.DataFrame)
        assert not df.empty
        assert len(df.columns) > 2
        assert len(df) > 0

    @pytest.mark.skipif
    def test_encoding(self):
        common_encodings = [
            'utf-8',
            'iso-8859-1',
            'cp1252',
            'Windows-1252',
        ]  # Add more if needed

        detected_encoding = chardet.detect(open(dbc_file, 'rb').read())[
            'encoding'
        ]
        self.assertIn(
            detected_encoding, common_encodings
        )  # Check if detected encoding is in the list

    def test_dbc_file_header(self):
        dbc_file = str(data_files / "STPI2206.dbc")
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

    def assertDataFrameValid(self, df):
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertGreater(len(df.columns), 0)
        self.assertGreater(len(df), 0)


if __name__ == '__main__':
    unittest.main()
