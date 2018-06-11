Mapped config
=============

[![Build Status](https://travis-ci.org/maxpowel/mapped_config.svg?branch=master)](https://travis-ci.org/maxpowel/mapped_config)

How to install
---------------
pip install mapped_config

What is this?
-------------
A configuration loader that loads, checks and build an structured configuration data object.

Why?
-----
When an application gets bigger the configuration grows too. Having a fully centralized system is not good because
it gets very hard to maintain. Also using dictionaries can provoke errors about accessing attributes or deprecated
and new attributes.

With mapped config you can delegate to every module the task of validate his own configuration. By this way, changes
 in one module only affects to this module.
 
You an also validate that your configuration file correct: no extra fields neither forget new fields. The software has
a continuous evolution process and add new configuration or deprecate the older ones is very common. By using mapped config
you can be sure that your configuration is up to date.

The other objective of this library is avoid error when accessing the configuration properties. Its common to use dictionaries but it
has a big problem: you should remember the keys or use a lot of constants. This is not cool when programming and your code gets a lot of
unnecessary extra weight. Explore the config possibilities its a nightmare because a dict can hold everything and can change by one one y any
moment.
Mapped config builds an structured object that can be easily inspected and no one can edit this configuration. Since the configuration object
is built with namedtuples it is readonly, efficient, friendly and easy to use and everything without external dependencies (namedtuples are great!).

How it works
------------
You only need an example to understand it. In this example we have config.yml that contains the application configuration, parameters.yml that has
 the constants (and are not commited to git) the example python code. Using parameters.yml is not mandatory but its very recommended.

config.yml
```yml
database:
  driver: {database_driver}
  hostname: {database_hostname}
  username: {database_password}
```

parameters.yml
```yml
database_driver: mysql
database_hostname: localhost
database_password: root

```

```python
from mapped_config.loader import YmlLoader

# Define the configuration schema for validation. Its simple and only
# validates if structure is fine
database_config_schema = {
    "database": {
        "driver": None, # None means no default value
        "hostname": "localhost", # Default value is localhost
        "username": "root",
        "password": "123456"
    }

}

yml_loader = YmlLoader()
config = yml_loader.load_config("example_simple_config.yml", "example_simple_parameters.yml")
# At this point we have the typical dictionary

mapped_config = yml_loader.build_config(config, [database_config_schema])
# Now the configuration is validated. If something is wrong, an exception is raised specifying 
# what field is wrong

# Now explore the configuration object
print(mapped_config)

database_config = mapped_config.database

print(database_config.hostname)
print(database_config.username)
print(database_config.password)
print(database_config.driver)

```
This will output
```
Configuration(database=database(username='root', hostname='localhost', password='123456', driver='mysql'))
localhost
root
123456
mysql
```


Features supported
------------------
Check the example.py or the tests to view how powerful it is. In summary you can:
* Simple attributes and default values
```python
database_config_schema = {
    "database": {
        "driver": None, # None means no default value
        "hostname": "localhost", # Default value is localhost
        "username": "root",
        "password": "123456"
    }

}
```

```yml
database:
  driver: localhost
  hostname: localhost
  username: root
  # The value password is missing here but has a default value
```

* Nested objects
```python
database_config_schema = {
    "database": {
        "driver": {
             "name": None,
             "version": None
        },
        "hostname": "localhost",
        "username": "root",
        "password": "123456"
    }

}
```

```yml
database:
  driver:
      name: mysql
      version: 5.0
  hostname: localhost
  username: root
```

* Lists with base types
```python
database_config_schema = {
    "database": {
        "driver": {
             "name": None,
             "versions": []
        }
    }

}
```

```yml
database:
  driver:
      name: mysql
      versions: [5.0, 10]
```

* Lists with objects
```python
database_config_schema = {
    "database": {
        "drivers": [{
             "name": None,
             "version": None
        }]
    }

}
```
Note that the drivers node is an array with only one element. This element
defines the structure of the elements that this node contains. To be able to
validate every element, you can only define one structure that is always the first element.
If no structure is specified, the validator assumes that id can contains everything (even raw dictionaries) 
If you specify two structures an exception will be raised

```yml
database:
  drivers:
      - name: mysql
        version: 5.0
      - name: postgres
        version: 6.0
      
```

* Mix everything
You can nest everything into everything. If you can build it with yml
you can map it

* Advanced validation
You can also check the data type
```python
database_config_schema = {
    "database": {
        "drivers": [{
             "name": {"type": "string"},
             "version": {"tỳpe": "integer", "default": 0}
        }]
    }

}
```

Schema constructor
------------------
Writing schemas like this is very simple and for small cases is enough. But because you have to write manually
the whole structure, it can contains errors like typos. You can avoid that using the schema constructor.

Manual schema definition
```python
database_config_schema = {
    "database": {
        "drivers": [{
             "name": {"type": "string"},
             "version": {"tỳpe": "integer", "default": 0}
        }]
    }

}
```
Equivalent with constructor
```python
from mapped_config import constructor
database_config_schema = constructor.MultiField(name="database", fields=[
    constructor.MultiField(name="drivers", fields=[
        constructor.StringField("name"),
        constructor.IntegerField("version", default=0)
    ])
])
```
You can build any structure with that.
* Simple field: StringField, IntegerField....
* Dictionary: MultiField
* List: ListField

You can check the file examples/raw_vs_classes_example.py to view more examples.

And thats all. You can check your final mapping by calling he method "build" of the constructor field.

Both ways (raw schema and constructor) are equals, just choose what more comfortable to you!

Can I use JSON?
---------------
Sure, just load the the JsonLoader instead of YmlLoader

```python
from mapped_config.loader import JsonLoader

database_config_schema = {
    "database": {
        "driver": None, # None means no default value
        "hostname": "localhost", # Default value is localhost
        "username": "root",
        "password": "123456",
        "port": None
    }

}

json_loader = loader.JsonLoader()
config = json_loader.load_config("example_simple_config.json", "example_simple_parameters.json")
mapped_config = json_loader.build_config(config, [database_config_schema])

print(mapped_config)

database_config = mapped_config.database

print(database_config.hostname)
print(database_config.username)
print(database_config.password)
print(database_config.driver)
```

Json uses braces which conflict with the replacement format used before.
The json loader replaces the braces {var} for the percent symbol %value%
 
example_simple_config.json
```json
{
  "database": {
          "driver": %database_driver%,
          "hostname": %database_hostname%,
          "username": %database_password%,
          "port": %database_port%
  }
}
```

example_simple_parameters.json
```json
{
  "database_driver": "mysql",
  "database_hostname": "localhost",
  "database_password": "root",
  "database_port": 566
}
```



Extending to other formats
--------------------------
I love YML but other people likes XML and other formats. To use them, just
extend the class ConfigurationLoader and implement its interface (just two methods
what basically converts your raw file into a dictionary).
You can mix formats and use json for config and yml for parameters or whatever you want,
just extend the base class and custom the load process.

Parameters preference
---------------------
You can also configure parameters by using environment variables (just use parameter as the env variable). From the lower to higher preference, the preferences are: default value, parameters file and parameters in environment variables

Tests
-----
Just run 

python mapped_config/test/test_schema_generator.py
