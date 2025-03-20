import unittest
from dataclasses import dataclass
import os
from src.read_config import config_reader

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class MyConfig:
    NAME: str
    PORT: int
    LOG_FILE: str


class NoDataclass:
    NAME: str
    PORT: int
    LOG_FILE: str


class ConfigReaderDataClassTestCase(unittest.TestCase):

    def test_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            config_reader(ROOT_DIR + "/mocks/config_1/my_defaults.ini", [])

        with self.assertRaises(AttributeError):
            config_reader(ROOT_DIR + "/mocks/config_1/my_defaults.ini", NoDataclass)

        c1 = config_reader(ROOT_DIR + "/mocks/config_1/my_defaults.ini")
        self.assertIsInstance(c1, dict)

        c2 = config_reader(ROOT_DIR + "/mocks/config_1/my_defaults.ini", MyConfig)
        self.assertIsInstance(c2, dict)


    def test_section_is_of_type_dict(self):
        reader = config_reader(ROOT_DIR + "/mocks/config_1/my_defaults.ini")
        config = reader.get('config2')
        self.assertIsInstance(config, dict)

    def test_section_is_mapped_to_given_dataclass(self):
        reader = config_reader(ROOT_DIR + "/mocks/config_1/my_defaults.ini", MyConfig)
        config: MyConfig = reader.get('config2')
        self.assertIsInstance(config, MyConfig)

        self.assertEqual("remote_server", config.NAME)
        self.assertEqual(80, config.PORT)
        self.assertEqual("/path/to/file.log", config.LOG_FILE)




if __name__ == '__main__':
    unittest.main()
