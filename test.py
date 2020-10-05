import unittest
import maths
import time

import file

"""
This file contains all of the unit tests for functions of the app.
Tests cover file.py and maths.py.

Last Updated: 02/10/2020
Author: Nathan Gillbanks
Contributors: Andrew Durnford
"""

class TestMethods(unittest.TestCase):

    # **************** file.py ******************

    # test read .bin file
    def test_binRead(self):
        data = file.binary_Read("test/UnitTest.bin")
        self.assertTrue(not data is None)

    def test_binReadException(self):
        with self.assertRaises(OSError):
            data = file.binary_Read("test/NotARealFile.bin")

    # test read .csv file
    def test_csvRead(self):
        data = file.binary_Read("test/UnitTest.csv")
        self.assertTrue(not data is None)

    def test_csvReadException(self):
        with self.assertRaises(OSError):
            data = file.csv_Read("test/NotARealFile.csv")

    # test read .data file
    def test_csvRead(self):
        data = file.data_read("test/UnitTest.data")
        self.assertTrue(not data is None)

    def test_csvReadException(self):
        with self.assertRaises(OSError):
            data = file.data_read("test/NotARealFile.data")

    # test read file 1
    def test_readFile1(self):
        post_calc = 1
        data = file.readFile("test/unitTest.data", post_calc)
        self.assertTrue(not data is None)

    # test read file 2
    def test_readFile2(self):
        post_calc = 2
        self.assertFalse(post_calc < 1)
        self.assertFalse(post_calc > 2)
        self.assertTrue(post_calc == 1 or post_calc == 2)
        post_calc = 1
        data = file.readFile("test/unitTest_Post.data", post_calc)
        self.assertTrue(not data is None)

    # **************** maths.py *****************

    def test_maths(self):
        data = file.readFile("./data/5ppm.data", 0)
        v = data.iloc[:, 0].values
        i = data.iloc[:, 1].values

        # test blanking_first_samples
        v, i = maths.blanking_first_samples(4000, v, i)
        self.assertEqual(len(i), len(v))

        # test get_time_values
        f, t = maths.get_time_values(i, 44100)
        self.assertEqual(len(f), len(t))

        # test get_ienv
        harmonic = maths.get_ienv(i, 60, 1, 10, 8000, 10, t)
        self.assertTrue(not harmonic is None)

        # test magnitude_of_current
        Imag = maths.magnitude_of_current(i, i.size)
        self.assertTrue(not Imag is None)

        # test cumulative_sum_ienv
        int_ienv = maths.cumulative_sum_ienv(harmonic)
        self.assertTrue(not int_ienv is None)

        # test filter_ienv
        ienv_filtered = maths.filter_ienv(harmonic, 200)
        self.assertTrue(not ienv_filtered is None)

if __name__ == '__main__':
    unittest.main()
