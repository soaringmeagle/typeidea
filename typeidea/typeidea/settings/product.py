from .base import *  # NOQA

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_db',
        'USER': 'root',
        'PASSWORD': '792028',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

ALLOWED_HOSTS = ['*']

STATIC_ROOT = '/home/meagle/www/typeidea-master/static' # Nginx静态文件目录


# REDIS_URL = '127.0.0.1:6379:1'
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_URL,
#         'TIMEOUT': 300,
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             # 'PARSER_CLASS':'redis.connection.HiredisParser',
#             'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
#         }
#     }
# }
