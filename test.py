import unittest

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
    # Helper.py: csv_read
    # Helper.py: data_read
    # Helper.py: readFile

if __name__ == '__main__':
    unittest.main()