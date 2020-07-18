import dj_database_url

from .settings import *


DEBUG = False

DATABASES = {
    'default': dj_database_url.config(),
}

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
