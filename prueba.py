import loader

yml_loader = loader.YmlLoader()

config = yml_loader.load_config("config.yml", "parameters.yml")

from collections import namedtuple

# queue = {
#     "_": namedtuple("queue", ["name", "number", "file_systems"]),
#     "file_systems": namedtuple("file_systems", ["mongo"]),
#     "file_systems_mongo": namedtuple("mongo", ["server", "username"]),
#     "handlers": [namedtuple("handler", ["namne", "version"])]
# }

queue = {
    "queue": {
        "name": "pepe",
        "number": {
            "moneda": None,
            "valor": None
        },
        "file_systems": {
            "mongo": {
                "server": {
                    "hostname": "localhost",
                    "port": 334
                },
                "username": None
            }
        },
        "handlers": [
            {
                "name": None,
                "version": {
                    "model": None,
                    "year": None
                }
            }
        ]
    }
}

queue = {
    namedtuple("queue", ["name", "number", "file_systems"]):
            {
                namedtuple("file_systems", ["mongo", "activar"]): {
                    namedtuple("mongo", ["server", "username"]): {
                        namedtuple("server", ["hostname", "port"]): None
                    }
                },
                namedtuple("number", ["moneda", "valor"]): None
            }#,
            #[{namedtuple("handlers", ["namne", "version"]): None}]

}

r = yml_loader.build_config(config, [queue, namedtuple("simple", ["saludo", "amigo"])])
print(r.queue)
