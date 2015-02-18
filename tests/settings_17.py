# This settings module is for Django 1.7 or higher
from settings import *  # NOQA

MIGRATION_MODULES = {
    'cms': 'cms.migrations_django',
}
