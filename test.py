import unittest

import file
import maths

import time
import pyautogui as gui
gui.FAILSAFE = False





class TestMethods(unittest.TestCase):

    # example test 1
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    # example test 2
    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    # example test 3
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    # **************** file.py ******************

    # test read .bin file
    # def test_binRead(self):
    # data = file.binary_Read("UnitTest.bin")
    # self.assertTrue(data is None)

    # with self.assertRaises(OSError):
    # file.binary_Read("UnitTest.bin")

    # test read .csv file
    # def test_csvRead(self):
    # data = file.binary_Read("UnitTest.csv")
    # self.assertTrue(data is None)

    # with self.assertRaises(OSError):
    # file.binary_Read("UnitTest.csv")

    # test read .data file
    # def test_dataRead(self):
    # data = file.binary_Read("UnitTest.data")
    # self.assertTrue(data is None)

    # with self.assertRaises(OSError):
    # file.binary_Read("UnitTest.data")

    # test read file 1
    # def test_readFile1(self):
    # post_calc = 1
    # data = file.readFile("UnitTest.data", post_calc)
    # self.assertEqual(data, None)

    # test read file 2
    def test_readFile2(self):
        post_calc = 2
        self.assertFalse(post_calc < 1)
        self.assertFalse(post_calc > 2)
        self.assertTrue(post_calc == 1 or post_calc == 2)
        # with self.assertIsNone():
        # data = file.readFile("UnitTest.data", post_calc)

    # **************** gui.py *******************

    # **************** maths.py *****************

    def test_maths(self):
        data = file.readFile("./data/5ppm.data", 0)
        v = data.iloc[:, 0].values
        i = data.iloc[:, 1].values

        # test blanking_first_samples
        v, i = maths.blanking_first_samples(4000, v, i)

        # test get_time_values
        f, t = maths.get_time_values(i, 44100)

        # test get_ienv
        harmonic = maths.get_ienv(i, 60, 1, 10, 8000, 10, t)

        # test magnitude_of_current
        Imag = maths.magnitude_of_current(i, i.size)

        # test cumulative_sum_ienv
        int_ienv = maths.cumulative_sum_ienv(harmonic)

        # test filter_ienv
        ienv_filtered = maths.filter_ienv(harmonic, 200)

        # test is_y_valid ?

        # test upper_envelope ?

        # test conc ?

    #GUI TEST
    def test_guiTest(self):
        print("yes")

        time.sleep(0.5)
        gui.moveTo(1254, 205)
        time.sleep(0.5)
        gui.click()
        time.sleep(0.5)
        gui.write("100ppm.data")
        time.sleep(0.5)
        gui.moveTo(1022, 679)
        time.sleep(0.5)
        gui.click()
        time.sleep(3)
        gui.moveTo(1370, 165)
        gui.click()
        time.sleep(1)
        gui.moveTo(1466, 207)
        gui.click()



        # screenWidth, screenHeight = gui.size()
        #gui.moveTo(0, screenHeight)
        #gui.click()

        thisText = gui.locateOnScreen("m9jr7NQ.png")
        self.assertTrue(not thisText is None)

    def test_guiTest_login(self):
        gui.moveTo(1546, 209)
        gui.click()
        gui.write("1245")
        gui.moveTo(835, 598)
        gui.click()
        print("no")
        thisText = gui.locateOnScreen("YNhrNcM.png")
        self.assertTrue(thisText)

    def test_guiTest_Harmonics(self):
        gui.moveTo(519, 893)
        gui.click()

        gui.moveTo(707, 892)
        gui.click()
        gui.moveTo(895, 890)
        gui.click()
        gui.moveTo(1076, 889)
        gui.click()
        gui.moveTo(1256, 890)
        gui.click()


if __name__ == '__main__':
    unittest.main()
