import unittest
import os
from src.read_config import config_reader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class ConfigReaderTestCase(unittest.TestCase):


    def test_raises_file_not_found_error(self):
        # test for single file
        with self.assertRaises(FileNotFoundError):
            config_reader("/some/missing/file.ini")

        with self.assertRaises(FileNotFoundError):
            config_reader([ROOT_DIR + "/mocks/config_1/base_config.ini", "/some/missing/file.ini"])


    def test_parses_single_config(self):
        c = config_reader(ROOT_DIR + "/mocks/config_1/my_defaults.ini")
        expected = {
            "config1": {"NAME": "localhost", "PORT": 12345, "LOG_FILE": "/tmp/config1.log"},
            "config2": {"NAME": "remote_server", "PORT": 80, "LOG_FILE": "/path/to/file.log"},
            "config3": {"NAME": "server_1", "PORT": 3000, "LOG_FILE": "123.log"},
            "config4": {"NAME": "server_2", "PORT": -2000, "LOG_FILE": "abc.log"},
            "config5": {"NAME": "server_2", "PORT": "-2000ABC", "LOG_FILE": "abc.log"},
        }
        self.assertEqual(expected, c)


    def test_parses_multiple_config(self):
        c = config_reader([ROOT_DIR + "/mocks/config_1/my_defaults.ini", ROOT_DIR + "/mocks/config_1/base_config.ini"])
        self.assertEqual(6, len(c))


    def test_last_config_wins(self):
        c = config_reader([
            ROOT_DIR + "/mocks/config_1/my_defaults.ini",
            ROOT_DIR + "/mocks/config_1/base_config.ini",
            ROOT_DIR + "/mocks/config_1/base_config_2.ini"
        ])
        self.assertEqual(8, len(c))
        expect_config_3_is_overwritten = {"NAME": "is_overwritten_twice", "PORT": 9090, "LOG_FILE": "/a/log/file.log"}
        self.assertEqual(expect_config_3_is_overwritten, c.get('config3'))


    def test_parses_values_correctly(self):
        c = config_reader([
            ROOT_DIR + "/mocks/config_1/my_defaults.ini",
            ROOT_DIR + "/mocks/config_1/base_config_2.ini"
        ])
        self.assertEqual(7, len(c))

        list_result = c.get('has_a_list')
        expect_list_result = {
            "NAME": "server_with_list",
            "PORT": 8080,
            "LOG_FILE": ["a", "b", -300, 0, 100]
        }
        self.assertEqual(expect_list_result, list_result)

        dict_result = c.get('has_a_dict')
        expect_list_result = {
            "NAME": "server_with_dict",
            "PORT": 12345,
            "LOG_FILE": {
                "a_log": "a.log",
                "b_log": "b.log",
                "is_number": -3000,
                # "is_list": ["a", "b", 1, 2, 3], NOT supported yet
            }
        }
        self.assertEqual(expect_list_result, dict_result)


    def test_cast_string_values_correct(self):
        c = config_reader(ROOT_DIR + "/mocks/config_1/types.ini")
        # has all sections
        self.assertEqual(6, len(c))

        self.assertIsInstance(c.get('STRINGS').get('IS_STRING'), str)
        self.assertEqual(c.get('STRINGS').get('IS_STRING'), "Hello World")

        self.assertIsInstance(c.get('STRINGS').get('IS_STRING2'), str)
        self.assertEqual(c.get('STRINGS').get('IS_STRING2'), "Hello World")

        self.assertIsInstance(c.get('STRINGS').get('IS_STRING3'), str)
        self.assertEqual(c.get('STRINGS').get('IS_STRING3'), "12345")

        self.assertIsInstance(c.get('STRINGS').get('IS_STRING4'), str)
        self.assertEqual(c.get('STRINGS').get('IS_STRING4'), "-9876")


    def test_cast_integer_values_correct(self):
        c = config_reader(ROOT_DIR + "/mocks/config_1/types.ini")
        self.assertIsInstance(c.get('INTEGERS').get('IS_POS_INT'), int)
        self.assertEqual(c.get('INTEGERS').get('IS_POS_INT'), 12345)
        self.assertIsInstance(c.get('INTEGERS').get('IS_NEG_INT'), int)
        self.assertEqual(c.get('INTEGERS').get('IS_NEG_INT'), -98765)


    def test_cast_list_values_correct(self):
        c = config_reader(ROOT_DIR + "/mocks/config_1/types.ini")

        self.assertIsInstance(c.get('LISTS').get('IS_LIST_OF_STRINGS'), list)
        self.assertIsInstance(c.get('LISTS').get('IS_LIST_OF_STRINGS2'), list)
        self.assertIsInstance(c.get('LISTS').get('IS_LIST_OF_POS_INT'), list)
        self.assertIsInstance(c.get('LISTS').get('IS_LIST_OF_NEG_INT'), list)
        self.assertIsInstance(c.get('LISTS').get('ANOTHER_LIST'), list)

        # value is in quotation marks, should be cast as string
        self.assertIsInstance(c.get('LISTS').get('IS_LIST_OF_STRINGS2')[0], str)
        self.assertIsInstance(c.get('LISTS').get('IS_LIST_OF_STRINGS2')[2], str)

        self.assertEqual(c.get('LISTS').get('IS_LIST_OF_STRINGS'), ["a", "b", "c", "d", "e"])
        self.assertEqual(c.get('LISTS').get('IS_LIST_OF_STRINGS2'), ["1", "2", "a", "b"])
        self.assertEqual(c.get('LISTS').get('IS_LIST_OF_POS_INT'), [1, 2, 3, 4, 5])
        self.assertEqual(c.get('LISTS').get('IS_LIST_OF_NEG_INT'), [-9, -8, -7, -6, -5])
        self.assertEqual(c.get('LISTS').get('ANOTHER_LIST'), [
            "item1",
            1234,
            -234,
            True,
            "123"
        ])






    def test_cast_dict_values_correct(self):
        c = config_reader(ROOT_DIR + "/mocks/config_1/types.ini")

        self.assertIsInstance(c.get('DICT').get('IS_DICT'), dict)
        self.assertEqual(c.get('DICT').get('IS_DICT'), {
            "key1": "value1",
            "key2": "value2",
            "int1": 123,
            "int2": -987
        })

    def test_cast_bool_values_correct(self):
        c = config_reader(ROOT_DIR + "/mocks/config_1/types.ini")

        # Test True values
        for n in range(1, 10):
            parameter = f"IS_BOOL_TRUE{n}"
            self.assertIsInstance(c.get('BOOL_TRUE').get(parameter), bool)
            self.assertEqual(c.get('BOOL_TRUE').get(parameter), True)

        # Test True values
        for n in range(1, 10):
            parameter = f"IS_BOOL_FALSE{n}"
            self.assertIsInstance(c.get('BOOL_FALSE').get(parameter), bool)
            self.assertEqual(c.get('BOOL_FALSE').get(parameter), False)




if __name__ == '__main__':
    unittest.main()
