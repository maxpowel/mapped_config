import loader

def load_kerner():
    return CoolFrameworkKernel()

def init():
    pass

class DatabaseManager(object):
    # Every module knows how is it own configuration
    config_mapping = {
        "database": {
            "default": None,
            "providers": [{
                "name": None,
                "hostname": "localhost",
                "username": "root",
                "password": 123456
            }]
        }
    }

    def __init__(self, configuration):
        self.config = configuration.database
        self.provider = self.config.providers[0]

    def session(self):
        print("Connection to {host} with {username}:{password}".format(
            host=self.provider.hostname,
            username=self.provider.username,
            password=self.provider
        ))




class PersistenceManager(object):
    config_mapping = {
        "persistence": {
            "amazon": {
                "bucket": None
            },
            "azure": {
                "storage": None
            },
            "local": {
                "directory": None
            }

        }
    }

    def __init__(self, configuration):
        self.config = configuration.persistence



class CryptoManager(object):
    config_mapping = {
        "crypto": {
            "magical_numbers": [],
            "best_algorithm": "random_for_the_lolz"
        }
    }
    def __init__(self, configuration):
        self.config = configuration.crypto


class QueueManager(object):
    config_mapping = {
        "queue": {
            "max_instances": 5,
            "workers": [{
                "name": None,
                "scheduler_plans": {
                    "low": [],
                    "high": [],
                }
            }]
        }
    }

    def __init__(self, configuration):
        self.config = configuration.queue


class CoolFrameworkKernel(object):
    registered_modules = [
        DatabaseManager, PersistenceManager, CryptoManager, QueueManager
    ]

    def __init__(self):
        yml_loader = loader.YmlLoader()
        # The kernel just load configuration and let every module validate it
        config = yml_loader.load_config("example_config.yml", "example_parameters.yml")
        self.config = yml_loader.build_config(config, [module.config_mapping for module in self.registered_modules])

    # Fake injection tool
    def inject(self, object_class):
        if object_class in self.registered_modules:
            return object_class(self.config)
        else:
            raise Exception("This module is not registered")