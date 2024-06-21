# Broker settings
broker_url = 'pyamqp://guest@localhost:5672//'

# List of modules to import when the Celery worker starts.
imports = ('tasks')

# Result backend
result_backend = 'rpc://'