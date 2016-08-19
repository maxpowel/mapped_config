import yaml
from abc import ABCMeta, abstractmethod
from collections import namedtuple

class NodeAlreadyConfiguredException(Exception):
    pass

class NodeIsNotConfiguredException(Exception):
    pass

class NodeHasNoMappingException(Exception):
    pass

class NodeMappingHasNoName(Exception):
    pass

class ConfigurationLoader(metaclass=ABCMeta):
    @abstractmethod
    def load_parameters(self, source):
        """Convert the source into a dictionary"""
        pass

    @abstractmethod
    def load_config(self, config_source, parameters_source):
        pass

    # def validate(self, config_map, validation_mappings):
    #     processed_nodes = set()
    #     for mapping in validation_mappings:
    #         name = mapping.__name__
    #         if name in config_map:
    #             if name in processed_nodes:
    #                 raise NodeAlreadyConfiguredException("Node {node} is already configured".format(node=name))
    #             else:
    #                 processed_nodes.add(name)
    #         else:
    #             raise NodeIsNotConfiguredException("Node {node} is not configured".format(node=name))
    #
    #     unprocessed_nodes = set(config_map.keys()).symmetric_difference(processed_nodes)
    #     if len(unprocessed_nodes):
    #         raise NodeHasNoMappingException("The following nodes has no mapping: {nodes}"
    #                                         .format(nodes=", ".join(list(unprocessed_nodes)))
    #                                         )

    def build_config(self, data, mapping):
        r = {}
        for i in mapping:
            # Root nodes
            r.update(self._build_root_node(i, data))
        # Convert data into namedtuple
        config_tuple = namedtuple("Configuration", r.keys())
        return config_tuple(**r)

    def _build_root_node(self, node, data):
        built_data = {}
        if isinstance(node, dict):
            # Es un tipo compuesto
            built_data.update(self._build_node_level(node, data))
        else:
            # Es un tipo simple
            built_data[node.__name__] = node(**self._get_node_data(node, data))
        return built_data

    def _build_node_level(self, node, data):
        built_data = {}
        for node_definition, sub_elements in node.items():
            node_name = node_definition.__name__
            node_built_data = {}
            node_data = self._get_node_data(node_definition, data)
            # Usamos mapped_sub_elemnts para que al recorrer los atributos de la namedtuple podamos buscar facilmente
            # si es un nodo hoja u otro subnodo
            if sub_elements is not None:
                # Tiene definicion para los atributos
                mapped_sub_elements = {s.__name__: s for s in sub_elements}
            else:
                # No tiene definicion, todos sus nodos son hoja
                mapped_sub_elements = {}

            for field in node_definition._fields:
                if field in mapped_sub_elements:
                    # Sub elemento
                    # Como estamos recorriendo usando el string field, mapped_sub_elements[field] contiene el namedtuple
                    # por el que está indexado el mapa de configuración

                    sub_element = sub_elements[mapped_sub_elements[field]]
                    if sub_element is None:
                        # Este sub elemento es un nodo hoja
                        node_built_data[field] = mapped_sub_elements[field](**node_data[field])
                    else:
                        node_built_data[field] = self._build_node_level(sub_element, node_data[field])

                else:
                    # El campo es nodo hoja
                    node_built_data[field] = node_data[field]

            built_data[node_name] = node_definition(**node_built_data)
        return built_data

    def _validate_node(self, node, data):
        # Root nodes are special because they dont have a parent. Here we start the recursion
        if not isinstance(node, dict):
            # Simple mapping
            return {node.__name__: node(**self._get_node_data(node, data))}
        else:
            # Complex mapping
            # First get the node name
            if "_" in node:
                return {node["_"].__name__: self._validate_level("_", node, self._get_node_data(node["_"], data))}
            else:
                raise NodeMappingHasNoName()

    """ Function to get node data or throw exception if no data for the node"""
    def _get_node_data(self, node, data, namespace=None):
        node_name = node.__name__
        if node_name not in data:
            raise NodeIsNotConfiguredException("Node {node} is not configured".format(node=node_name))
        else:
            return data[node_name] if namespace is None else data["{namespace}_{node_name}".format(namespace=namespace, node_name=node_name)]

    def _validate_level(self, attribute, node, data, namespace=None):
        node_structure = node[attribute]
        node_name = node_structure.__name__

        node_built_data = {}
        # Check every field of the namedtuple
        for field in node_structure._fields:
            namespaced = namespace if namespace is not None else "" + "_" + field
            if field in node or namespaced in node:
                if namespaced in node:
                    field = namespaced
                # Is an another node
                print("{field} es otro nodo".format(field=field))
                new_namespace = field if namespace is None else "{parent}_{me}".format(parent=namespace, me=field)
                node_built_data[field] = self._validate_level(new_namespace, node, self._get_node_data(node[field], data, namespace), new_namespace)
                #node_built_data[field] = new_namespace
            else:
                # Is a leaf node
                print("{field} es hoja".format(field=field))
                node_built_data[field] = data[field]
        return node_structure(**node_built_data)



        #main = namedtuple('Configuration', load_mappings(mapping_modules))


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



# Testear, complex mapping sin node name (el de _)
# Testear que el complex no está configurado