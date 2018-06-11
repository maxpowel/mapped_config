# This example shows the equivalent mapping between raw mapping (create manually the schema) and the schema built
# using the schema constructorz

from mapped_config.loader import build_config
from mapped_config import InvalidDataException

mapped_schema = {
    "mysql": None,
    "port": 34190,
    "auth": {
        "username": {
            "type": "float",
            "default": "root"
        },
        "password": None

    },
    "hosts": [{"ip": {"type":"string"}, "port": 123}],
    "names": [{"type": "string"}]
}


document = {
    "mysql": "si",
    "port": 12,
    "auth": {
        "password": "123",
        "username": "23"
    },
    #"caca": "futi",
    "hosts": [
        {"ip":"12", "port":12}
    ],
    "names": ["pepe", 123]

}


try:
    c = build_config(mapped_schema, document)
    print(c)
except InvalidDataException as e:
    for i in e.errors:
        print(i)


# Con lo otro

from mapped_config import constructor

fields = constructor.MultiField([
    constructor.IntegerField(name="port", default=34190),
    constructor.StringField(name="mysql"),
    constructor.ListField(name="names"),
    constructor.ListField(name="hosts", field=constructor.MultiField(fields=[
        constructor.StringField(name="ip"),
        constructor.IntegerField(name="port", default=123)
    ])),
    constructor.MultiField(name="auth", fields=[
        constructor.StringField(name="password"),
        constructor.FloatField(name="username", default="root")
    ])
])

try:
    c = build_config(fields.build(), document)
    print(c)
except InvalidDataException as e:
    for i in e.errors:
        print(i)

