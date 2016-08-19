class DatabaseManager(object):
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

    def connect(self):
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
                "storeage": None
            },
            "local": {
                "directory": None
            }

        }
    }



class CryptoManager(object):
    config_mapping = {
        "crypto": {
            "magical_numbers": [],
            "best_algorithm": "random_for_the_lolz"
        }
    }

class QueueManager(object):
    config_mapping = {
        "queue": {
            "max_instances": 5,
            "workers": [{
                "name": None,
                "scheduler_plans": {
                    "low": [1],
                    "medium": [5],
                    "high": [10],
                }
            }]
        }
    }
