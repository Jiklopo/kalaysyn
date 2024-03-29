from os import getenv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

def init_sentry():
    SENTRY_KEY = getenv('SENTRY_KEY', None)
    if not SENTRY_KEY:
        return

    sentry_sdk.init(
        dsn=SENTRY_KEY,
        integrations=[DjangoIntegration()],

        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,

        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True,

        # By default the SDK will try to use the SENTRY_RELEASE
        # environment variable, or infer a git commit
        # SHA as release, however you may want to set
        # something more human-readable.
        # release="myapp@1.0.0",
    )
