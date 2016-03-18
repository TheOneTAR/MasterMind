import os

from .settings import BASE_DIR

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zv@ed+pnip5m$rcx43qec@&pu2-7^!j%@2*vclmzh*5g%a7v_#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
