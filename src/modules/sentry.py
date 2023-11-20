import raven

# Assuming config is a module with a sentryDSN attribute
from your_module_path.config import sentryDSN

client = raven.Client(sentryDSN)

def sentry(string, obj, error):
    with client.context() as ctx:
        ctx.user = {'string': string, 'object': obj}
        client.captureException(error)

def sentry_error(error):
    client.captureException(error)

def sentry_message(message):
    client.captureMessage(message)

def sentry_error_handler():
    return raven.fetch_raven_error_handler(client)

def sentry_request_handler():
    return raven.fetch_raven_request_handler(client)


