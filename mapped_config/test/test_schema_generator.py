from mapped_config.loader import build_config, InvalidDataException, mapped_to_cerberus
from mapped_config.constructor import MultiField, IntegerField, StringField, ListField
from mapped_config import loader
import os
import unittest
import six

class TestSchemaGenerator(unittest.TestCase):

    def test_simple_object(self):
        mapped_schema = {
            "number": 12345,
        }

        data = {
            "number": 56
        }

        c = build_config(mapped_schema, data)
        self.assertEqual(c.number, data["number"])

        with self.assertRaises(InvalidDataException):
            build_config(mapped_schema, {"number": "string"})

        # Extra field
        with self.assertRaises(InvalidDataException):
            build_config(mapped_schema, {"number": 123, "extra_field": "testing"})

    def test_nested_object(self):
        schema = {
            "auth": {
                "username": {
                    "type": "string",
                    "default": "root"
                }
            }
        }

        data = {
            "auth": {
                "username": "user"
            }
        }
        c = build_config(schema, data)
        self.assertEqual(c.auth.username, data["auth"]["username"])

        # Default value
        c = build_config(schema, {})
        self.assertEqual(c.auth.username, "root")

        with self.assertRaises(InvalidDataException):
            build_config(schema, {"auth": {"username": 123}})

    def test_list(self):
        schema = {"hosts": [{"ip": {"type": "string"}, "port": 123}]}
        data = {"hosts": [{"ip": "192.168.2.1", "port": 5000}, {"ip": "192.168.2.4", "port": 6000}]}

        c = build_config(schema, data)
        self.assertEqual(c.hosts[1].ip, data["hosts"][1]["ip"])
        with self.assertRaises(InvalidDataException):
            build_config(schema, {"hosts": [{"ip": "192.168.2.4", "port": "6000"}]})

    def test_none(self):

        self.assertDictEqual(mapped_to_cerberus({"field": None}), {'field': {'required': True}})

# The same but using the schema consctructor
if six.PY3:
    class TestSchemaConstructor(unittest.TestCase):

        def test_simple_object(self):
            mapped_schema = MultiField([IntegerField("number", 12345)])

            data = {
                "number": 56
            }

            c = build_config(mapped_schema, data)
            self.assertEqual(c.number, data["number"])

            with self.assertRaises(InvalidDataException):
                build_config(mapped_schema, {"number": "string"})

            # Extra field
            with self.assertRaises(InvalidDataException):
                build_config(mapped_schema, {"number": 123, "extra_field": "testing"})

        def test_nested_object(self):

            schema = MultiField([
                MultiField(name="auth", fields=[
                    StringField("username", "root")
                ])
            ])

            data = {
                "auth": {
                    "username": "user"
                }
            }
            c = build_config(schema, data)
            self.assertEqual(c.auth.username, data["auth"]["username"])

            # Default value
            c = build_config(schema, {})
            self.assertEqual(c.auth.username, "root")

            with self.assertRaises(InvalidDataException):
                build_config(schema, {"auth": {"username": 123}})

        def test_list(self):
            schema = MultiField([
                ListField("hosts", MultiField([
                    StringField("ip", "192.168.2.1"),
                    IntegerField("port", 5000)
                ]))
            ])
            data = {"hosts": [{"ip": "192.168.2.1", "port": 5000}, {"ip": "192.168.2.4", "port": 6000}]}

            c = build_config(schema, data)
            self.assertEqual(c.hosts[1].ip, data["hosts"][1]["ip"])
            with self.assertRaises(InvalidDataException):
                build_config(schema, {"hosts": [{"ip": "192.168.2.4", "port": "6000"}]})


class TestYmlLoader(unittest.TestCase):
    dir_path = os.path.dirname(os.path.realpath(__file__))

    def test_load_parameters(self):
        yml_loader = loader.YmlLoader()
        test_parameters = yml_loader.load_parameters(os.path.join(self.dir_path,"parameters.yml"))
        real_parameters = {
            "database_host": "'localhost'",
            "database_username": "'root'",
            "a_pretty_list": [1, 2, {"who_am_i": "an object"}]
        }
        self.assertDictEqual(real_parameters, test_parameters, "Parameters were not loaded correctly")

    def test_load_config(self):
        yml_loader = loader.YmlLoader()
        test_config = yml_loader.load_config(os.path.join(
            self.dir_path,"config.yml"),
            os.path.join(self.dir_path, "parameters.yml")
        )
        real_config = {
            "database": {
                "host": "localhost",
                "username": "root",
                "static": "Im static"
            }
        }

        self.assertDictEqual(real_config, test_config, "Config data was not loaded correctly")

if __name__ == '__main__':
    unittest.main()
