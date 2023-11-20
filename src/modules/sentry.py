import sentry_sdk
from dotenv import dotenv_values

config = dotenv_values()

sentry_sdk.init(
    dsn=config['SENTRY_DSN'],

    # Enable performance monitoring
    enable_tracing=True,
)

def sentry(info, object, error):
    with sentry_sdk.push_scope() as scope:
        scope.set_tag(info, object)
        scope.level = 'warning'
        sentry_sdk.capture_exception(error)


def sentryMessage(message: str):
    sentry_sdk.capture_message(message)

def sentryError(error):
    sentry_sdk.capture_exception(error)

