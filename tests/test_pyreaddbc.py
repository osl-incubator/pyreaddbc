import os
import unittest

import pandas as pd

from . import read_dbc_dbf

PATH_ROOT = os.path.dirname(os.path.abspath(__file__))


class TestReadDbcToDBF(unittest.TestCase):
    def test_read_dbc_dbf(self):

        dbc_name = PATH_ROOT + "/" + "data" + "/" + "ZIKABR16.DBC"
        df = read_dbc_dbf(dbc_name)

        self.assertTrue(os.path.exists(dbc_name))
        self.assertIsInstance(df, pd.DataFrame)
