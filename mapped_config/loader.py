import yaml
import json
import re
from abc import ABCMeta, abstractmethod
from collections import namedtuple


class NodeIsNotConfiguredException(Exception):
    pass


class NoValueException(Exception):
    pass


class IgnoredFieldException(Exception):
    pass


class ConfigurationLoader(metaclass=ABCMeta):
    @abstractmethod
    def load_parameters(self, source):
        """Convert the source into a dictionary"""
        pass

    @abstractmethod
    def load_config(self, config_source, parameters_source):
        pass

    def build_config(self, data, mapping, as_namedtuple=True):
        r = {}
        for i in mapping:
            # Root nodes
            r.update(self._build_node_config(node_info=i, node_data=data, as_namedtuple=as_namedtuple))
        # Convert data into namedtuple
        config_tuple = namedtuple("Configuration", r.keys())
        # warn about unsued root nodes configuration
        extra_fields = set(data.keys()).difference(set(r.keys()))

        if len(extra_fields) > 0:
            raise IgnoredFieldException("The root nodes [{nodes}] are ignored in your mapping".format(nodes=", ".join(extra_fields)))
        return config_tuple(**r)

    def _build_node_config(self, node_info, node_data, namespace=None, as_namedtuple=True):
        built_config = {}
        # This set is used to check unsued configuration
        processed_nodes = set()

        for node, node_content in node_info.items():
            processed_nodes.add(node)
            new_namespace = "{namespace}:{node}".format(namespace=namespace, node=node) if namespace is not None else node
            if isinstance(node_content, dict):
                # Node
                d = self._get_node_data(node, node_data, namespace)
                built_config[node] = self._build_node_config(node_content, d, "{namespace}:{node}".format(namespace=namespace, node=node) if namespace is not None else node, as_namedtuple)
            elif isinstance(node_content, list):
                # List node
                node_len = len(node_content)
                if node_len == 0:
                    # Simple list
                    d = self._get_node_data(node, node_data, "{namespace}:{node}".format(namespace=namespace, node=node) if namespace is not None else node)
                    built_config[node] = d
                elif node_len == 1:
                    # Object list
                    # The node structure is defined in the first element
                    node_structure = node_content[0]
                    node_config_processed = []
                    d = self._get_node_data(node, node_data, namespace)
                    for index in range(len(d)):
                        # The wrong element is specified by using it index
                        node_config_processed.append(self._build_node_config(node_structure, d[index], new_namespace+"_"+str(index), as_namedtuple))

                    built_config[node] = node_config_processed
                else:
                    raise Exception("Object list mapping should have only one element at {node}".format(node=node))
            else:
                # Leaf node
                if node in node_data:
                    # The specified value in the configuration
                    built_config[node] = self._get_node_data(node, node_data, namespace)
                elif node_content is not None:
                    # The default value specified in the mapping, if any
                    built_config[node] = node_content
                else:
                    raise NoValueException("No value for node {node}".format(node=new_namespace))

        # Only check if it is not the root node because every root node sees as "ignored" others roots nodes
        if namespace is not None:
            extra_fields = list(set(node_data.keys()).difference(processed_nodes))
            if len(extra_fields) > 0:
                with_namespace = ["{namespace}:{field}".format(namespace=namespace, field=field)for field in extra_fields]
                raise IgnoredFieldException(
                    "The nodes [{nodes}] are ignored in your mapping".format(nodes=", ".join(with_namespace)))

        if as_namedtuple:
            if namespace is None:
                # Root, return as dict
                return built_config
            else:
                name = namespace.split(":")[-1]
                node_namedtumple = namedtuple(name, built_config.keys())
                return node_namedtumple(**built_config)
        else:
            return built_config

    """ Function to get node data or throw exception if no data for the node"""
    def _get_node_data(self, node, data, namespace):
        if node not in data:
            raise NodeIsNotConfiguredException("Node {namespace}:{node} is not configured".format(node=node, namespace=namespace))
        else:
            return data[node]


class YmlLoader(ConfigurationLoader):
    def load_parameters(self, source):
        """For YML, the source it the file path"""
        with open(source) as parameters_source:
            return yaml.safe_load(parameters_source.read())

    def load_config(self, config_source, parameters_source):
        """For YML, the source it the file path"""
        with open(config_source) as config_source:
            config_raw = config_source.read()
            """Replace the parameters"""
            final_configuration = config_raw.format(**self.load_parameters(parameters_source))
            return yaml.safe_load(final_configuration)

class JsonLoader(ConfigurationLoader):
    def __init__(self):
        self.parameters = None

    def load_parameters(self, source):
        """For JSON, the source it the file path"""
        with open(source) as parameters_source:
            return json.loads(parameters_source.read())

    def load_config(self, config_source, parameters_source):
        """For JSON, the source it the file path"""
        with open(config_source) as config_source:
            config_raw = config_source.read()
            """Replace the parameters"""
            pattern = "(%[a-zA-Z_0-9]*%)"
            self.parameters = self.load_parameters(parameters_source)
            replaced_config = re.sub(pattern=pattern, repl=self._replace_function, string=config_raw)
            return json.loads(replaced_config)

    def _replace_function(self, match):
        # Remove % from the begining and from the end
        parameter_key = match.group(0)[1:-1]
        value = self.parameters[parameter_key]
        # Add the " for string values
        return str(value) if str(value).isdigit() else '"{value}"'.format(value=value)
