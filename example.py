import loader

def ConfigurationManager
yml_loader = loader.YmlLoader()

config = yml_loader.load_config("example_config.yml", "example_parameters.yml")

r = yml_loader.build_config(config, [queue, simple])
print(r)
