# -*- coding: utf-8 -*-
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# This allows requests from all hosts, this is temporary, it will be changed to a specific ip
ALLOWED_HOSTS = ['*']

STATIC_ROOT = os.path.join(BASE_DIR, "../static/")
