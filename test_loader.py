import unittest
import loader
from collections import namedtuple

class TestYmlLoader(unittest.TestCase):

    def test_load_parameters(self):
        yml_loader = loader.YmlLoader()
        test_parameters = yml_loader.load_parameters("test/parameters.yml")
        real_parameters = {
            "database_host": "localhost",
            "database_username": "root",
            "a_pretty_list": [1, 2, {"who_am_i": "an object"}]
        }
        self.assertDictEqual(real_parameters, test_parameters, "Parameters were not loaded correctly")

    def test_load_config(self):
        yml_loader = loader.YmlLoader()
        test_config = yml_loader.load_config("test/config.yml", "test/parameters.yml")
        real_config = {
            "database": {
                "host": "localhost",
                "username": "root",
                "static": "Im static"
            }
        }

        self.assertDictEqual(real_config, test_config, "Config data was not loaded correctly")


class TestConfigurationLoader(unittest.TestCase):

    def test_invalid_nodes(self):
        yml_loader = loader.YmlLoader()
        config = yml_loader.load_config("test/config.yml", "test/parameters.yml")
        # Some mapping examples
        database = namedtuple("database", ["name", "number", "file_systems"])
        queue = namedtuple("queue", ["name", "number", "file_systems"])
        database_again = database

        with self.assertRaises(loader.NodeHasNoMappingException):
            yml_loader.validate(config, [])

        with self.assertRaises(loader.NodeIsNotConfiguredException):
            yml_loader.validate(config, [queue])

        with self.assertRaises(loader.NodeAlreadyConfiguredException):
            yml_loader.validate(config, [database, database_again])

    def test_successful(self):
        yml_loader = loader.YmlLoader()
        config = yml_loader.load_config("test/config.yml", "test/parameters.yml")
        database = namedtuple("database", ["name", "number", "file_systems"])
        # Should not raise exception
        yml_loader.validate(config, [database])



