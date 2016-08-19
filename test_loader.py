import unittest
import loader


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


class TestConfigurationBuilder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.loader = loader.YmlLoader()

    def load_case_test(self, case):
        return self.loader.load_config(
            "test/{case}_config.yml".format(case=case),
            "test/parameters.yml",
        )

    def test_no_data_nodes(self):
        config = self.load_case_test("no_leaf_simple")
        # None value means no default, requiered value
        # Any other value means that this is the default value
        database = {
            "database": {
                "host": "localhost",
                "username": None
            }
        }
        with self.assertRaises(loader.NoValueException):
            # Raise because username is not in the config and neither have a default value
            self.loader.build_config(config, [database])

    def test_default_data(self):
        config = self.load_case_test("no_leaf_simple")
        database = {
            "database": {
                "host": "localhost",
                "username": "default_username"
            }
        }
        r = self.loader.build_config(config, [database])
        # In the maping the username field has a defaulf value
        self.assertEqual(r.database.username, database["database"]["username"])

    def test_extra_attribute(self):
        config = self.load_case_test("extra_attribute")
        database = {
            "database": {
                "host": "localhost",
                "username": "default_username"
            }
        }

        with self.assertRaises(loader.IgnoredFieldException):
            # Raise because the field weird_password is in the config file but not in the config mapping
            self.loader.build_config(config, [database])

        config = self.load_case_test("extra_attribute_root")
        with self.assertRaises(loader.IgnoredFieldException):
            # In this case, is an extra root node
            self.loader.build_config(config, [database])

    def test_nested_object(self):
        config = self.load_case_test("nested_object")
        queue = {
            "queue": {
                "name": None,
                "money": {
                    "currency": None,
                    "value": None
                }
            }
        }
        r = self.loader.build_config(config, [queue])
        self.assertEqual(r.queue.name, "caa")
        self.assertEqual(r.queue.money.currency, "euro")
        self.assertEqual(r.queue.money.value, 3)

        # Now a double nested because you dont trust me!
        config = self.load_case_test("double_nested_object")
        queue = {
            "queue": {
                "name": None,
                "money": {
                    "currency": None,
                    "value": None,
                    "validity": {
                        "start": 99,
                        "end": 199
                    }
                }
            }
        }
        r = self.loader.build_config(config, [queue])
        self.assertEqual(r.queue.name, "caa")
        self.assertEqual(r.queue.money.currency, "euro")
        self.assertEqual(r.queue.money.value, 3)
        self.assertEqual(r.queue.money.validity.start, 10)
        self.assertEqual(r.queue.money.validity.end, 20)

    def test_nested_object_ignored(self):

        config = self.load_case_test("double_nested_object")
        queue = {
            "queue": {
                "name": None,
                "money": {
                    "currency": None,
                    "value": None
                }
            }
        }

        with self.assertRaises(loader.IgnoredFieldException):
            # The validity node is in config but not in the mapping
            self.loader.build_config(config, [queue])

        config = self.load_case_test("nested_object")
        queue = {
            "queue": {
                "name": None,
                "money": {
                    "currency": None,
                    "value": None,
                    "who": {
                        "you": None,
                        "me": None
                    }

                }
            }
        }

        with self.assertRaises(loader.NodeIsNotConfiguredException):
            # The who node is in mapping but not in the config
            self.loader.build_config(config, [queue])

    def test_list(self):
        config = self.load_case_test("list")
        main = {
            "main": {
                "numbers": []
            }
        }

        r = self.loader.build_config(config, [main])
        self.assertIsNotNone(r.main)
        self.assertEqual(len(r.main.numbers), 5)
        self.assertEqual(r.main.numbers[0], 1)
        self.assertEqual(r.main.numbers[1], 2)
        self.assertEqual(r.main.numbers[2], 4)
        self.assertEqual(r.main.numbers[3], 8)
        self.assertEqual(r.main.numbers[4], "inf")

    def test_list_with_objects(self):
        config = self.load_case_test("list_objects")
        main = {
            "main": {
                "users": [
                    {
                        "name": None,
                        "age": None,
                        "enabled": True
                    }
                ]
            }
        }

        r = self.loader.build_config(config, [main])
        self.assertIsNotNone(r.main)
        self.assertEqual(len(r.main.users), 2)
        self.assertDictEqual(r.main.users[0]._asdict(), {"name": "pepe", "age": 96, "enabled": True})
        self.assertDictEqual(r.main.users[1]._asdict(), {"name": "ose lui", "age": 22, "enabled": True})

    def test_list_with_objects_multiple_mapping_error(self):
        config = self.load_case_test("list_objects")
        main = {
            "main": {
                "users": [
                    {
                        "name": None,
                        "age": None
                    },
                    {
                        "lol": True
                    }
                ]
            }
        }

        with self.assertRaises(Exception):
            # The validity node is in config but not in the mapping
            self.loader.build_config(config, [main])

    def test_full_example_ok(self):
        # Load a full example, everything should be ok because we tested every part individually
        config = self.load_case_test("full_ok")

        queue = {
            "queue": {
                "name": None,
                "number": {
                    "currency": None,
                    "value": None
                },
                "file_systems": {
                    "mongo": {
                        "server": {
                            "hostname": "localhost",
                            "port": 45
                        },
                        "username": None
                    }
                },
                "handlers": [{
                    "name": None,
                    "version": {
                        "model": None,
                        "year": None
                    },
                    "years": [],
                    "months": [],
                }]

            }
        }

        simple = {
            "simple": {
                "greet": None,
                "friend": "of mine"
            }
        }
        r = self.loader.build_config(config, [queue, simple])
        self.assertEqual(r.queue.name, "caa")
        self.assertEqual(r.queue.file_systems.mongo.server.port, 344)
        self.assertEqual(len(r.queue.handlers), 2)
        self.assertEqual(r.simple.greet, "hello")
        self.assertEqual(r.simple.friend, "of mine")

        # Now we test with some extra config
        config = self.load_case_test("full_extra")
        with self.assertRaises(loader.IgnoredFieldException):
            # Raise because the field weird_password is in the config file but not in the config mapping
            self.loader.build_config(config,  [queue, simple])

        # Now with insufficient config (remove the name attribute which is mandatory)
        config = self.load_case_test("full_extra_mapping")
        with self.assertRaises(loader.NoValueException):
            # Raise because the field weird_password is in the config file but not in the config mapping
            self.loader.build_config(config,  [queue, simple])

