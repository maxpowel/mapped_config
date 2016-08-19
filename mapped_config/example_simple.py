import loader

database_config_schema = {
    "database": {
        "driver": None, # None means no default value
        "hostname": "localhost", # Default value is localhost
        "username": "root",
        "password": "123456"
    }

}

yml_loader = loader.YmlLoader()
config = yml_loader.load_config("example_simple_config.yml", "example_simple_parameters.yml")
mapped_config = yml_loader.build_config(config, [database_config_schema])

print(mapped_config)

database_config = mapped_config.database

print(database_config.hostname)
print(database_config.username)
print(database_config.password)
print(database_config.driver)
