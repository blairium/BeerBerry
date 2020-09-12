import unittest
import File


class TestStringMethods(unittest.TestCase):

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

    # **************** UNIT TESTS ******************
    # And_AC_Volt_Python: major_function
    # And_AC_Volt_Python: get_time_values

    # Helper.py: get_time_values
    # Helper.py: binary_Read

    def test_binRead(self):
        data = File.binary_Read("UnitTest.bin")
        self.assertTrue(data is None)

        with self.assertRaises(OSError):
            File.binary_Read("UnitTest.bin")

    # Helper.py: csv_read

    def test_binRead(self):
        data = File.binary_Read("UnitTest.csv")
        self.assertTrue(data is None)

        with self.assertRaises(OSError):
            File.binary_Read("UnitTest.csv")

    # Helper.py: data_read
    def test_binRead(self):
        data = File.binary_Read("UnitTest.data")
        self.assertTrue(data is None)

        with self.assertRaises(OSError):
            File.binary_Read("UnitTest.data")

    # Helper.py: readFile

    def test_readFile1(self):
        post = 1
        data = File.readFile("UnitTest.data", post)
        self.assertEqual(data, None)

    # Helper.py: readFile2
    def test_readFile2(self):
        post = 2
        self.assertTrue(post == 1)
        self.assertTrue(post == 0)
        self.assertFalse(post == 2)
        with self.assertIsNone():
            data = File.readFile("UnitTest.data", post)


if __name__ == '__main__':
    unittest.main()
