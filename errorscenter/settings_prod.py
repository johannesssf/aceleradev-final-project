import dj_database_url

from .settings import *


DEBUG = False

DATABASES = {
    'default': dj_database_url.config(),
}
