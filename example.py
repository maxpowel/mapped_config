import example_modules
# THIS A FAKE EXAMPLE
# In this example I show how this module can be integrated into a real environment. Everything but the config is fake and
# does not have any functionality, its just a mockup

# App initilizacion
example_modules.init()
kernel = example_modules.load_kerner()

# In the injection the configuration are passed to the module, check it in the examples_modules.py file
database_manager = kernel.inject(example_modules.DatabaseManager)

# Doing some stuff with this service
database_manager.session()


file_system = kernel.inject(example_modules.PersistenceManager)
print(file_system.config)

queue_manager = kernel.inject(example_modules.QueueManager)
print("There are {n} workers configured:".format(n=len(queue_manager.config.workers)))
for worker in queue_manager.config.workers:
    print("\tWorker {name}".format(name=worker.name))
