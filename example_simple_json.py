import loader

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
