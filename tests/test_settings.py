"""module contains settings for tests project"""

VISUAL_CROSSING_API_KEY='dummy_api_key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

CACHES = {
    "default": {
        "BACKEND": 'django.core.cache.backends.dummy.DummyCache',
    }
}
