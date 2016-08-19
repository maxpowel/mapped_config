from collections import namedtuple

# Main configuration
main = namedtuple('Configuration', load_mappings(mapping_modules))


#Load configuration dynamically
def load_mappings(mapping_modules):
    # Core sections, the configuration sections required by the base system
    core_sections = ['fluent', 'sentry', 'entity_persistence', 'document_persistence', 'queue']

    # Iterate the namespaces defined in config.py where are added extra files where are located others mappings
    for module_name in mapping_modules:
        module = importlib.import_module(module_name)
        module_mapping_list = module.register()
        core_sections.append(module.name)
        for name, obj in inspect.getmembers(module):
            # Load all elements that are clases (namedtuples). The element should be a class
            # and defined in 'register' list. This is because you an load third party classes (for whatever reason)
            # but should not be treated as configuration mapping
            if inspect.isclass(obj) and name in module_mapping_list:
                # Finally add the mapping to the module (which will be used by the configuration loader)
                globals()[name] = obj

    # At this moment this module has all mappings from all modules
    return core_sections