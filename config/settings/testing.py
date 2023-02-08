from .default import *

DEBUG = True

INTERNAL_IPS = ["127.0.0.1"]

SOUTH_TESTS_MIGRATE = False

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3"}}
