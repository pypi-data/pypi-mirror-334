import environ
from azure.keyvault.secrets import SecretClient

from .azure_helper import AZURE_CREDENTIAL, LOCAL_IP_ADDRESSES, get_db_password, get_redis_credentials, get_subscription

env = environ.Env()

SECRET_KEY = env("DJANGO_SECRET_KEY")

# Health check path
HEALTH_CHECK_PATH = env("HEALTH_CHECK_PATH", default="/health")

ALLOWED_HOSTS: list = env.list("DJANGO_ALLOWED_HOSTS", default=[])
# WEBSITE_HOSTNAME contains the Azure domain name
ALLOWED_HOSTS.append(env("WEBSITE_HOSTNAME"))
# Add the local IP addresses of the machine for health checks
ALLOWED_HOSTS.extend(LOCAL_IP_ADDRESSES)

# Detect HTTPS behind AppService
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


# Azure context
AZURE_SUBSCRIPTION = get_subscription()
AZURE_TENANT_ID = AZURE_SUBSCRIPTION.tenant_id
AZURE_SUBSCRIPTION_ID = AZURE_SUBSCRIPTION.subscription_id

# Azure Key Vault
AZURE_KEY_VAULT = env("AZURE_KEY_VAULT")
AZURE_KEY_VAULT_URI = f"https://{AZURE_KEY_VAULT}.vault.azure.net"
AZURE_KEY_VAULT_CLIENT = SecretClient(vault_url=AZURE_KEY_VAULT_URI, credential=AZURE_CREDENTIAL)

# Allow CSRF cookies to be sent from our domains
# CSRF_TRUSTED_ORIGINS = ["https://" + host for host in ALLOWED_HOSTS]
AZURE_ACCOUNT_NAME = env("AZURE_STORAGE_ACCOUNT_NAME")
AZURE_TOKEN_CREDENTIAL = AZURE_CREDENTIAL


# CDN domain - shared for all storages
AZURE_CUSTOM_DOMAIN = env("CDN_HOST")

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "azure_container": env("AZURE_STORAGE_CONTAINER_MEDIA"),
            "overwrite_files": False,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "azure_container": env("AZURE_STORAGE_CONTAINER_STATICFILES"),
        },
    },
}


# STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = f"https://{AZURE_CUSTOM_DOMAIN}/static/"
MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/media/"

# This setting enables password rotation in the health check middleware
AZURE_DB_PASSWORD = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "HOST": env("DB_HOST"),
        "PASSWORD": get_db_password(),
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "require",
        },
        # Make connections persistent
        "CONN_MAX_AGE": None,
        # To enable health checks, add the following:
        # "CONN_HEALTH_CHECKS": True,
    }
}

# Email
EMAIL_BACKEND = "django_azure_communication_email.EmailBackend"
AZURE_COMMUNICATION_ENDPOINT = env("AZURE_COMMUNICATION_SERVICE_ENDPOINT")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "/home/LogFiles/django.log",
            "maxBytes": 1024 * 1024 * 100,  # 100 mb
            "backupCount": 5,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Redis, if enabled
if env("REDIS_CACHE_HOST") and env("REDIS_CACHE_PORT") and env("REDIS_CACHE_DB"):
    # This will enable the health check to update the Redis credentials
    AZURE_REDIS_CREDENTIALS = True

    # This will prevent the website from failing if Redis is not available
    DJANGO_REDIS_IGNORE_EXCEPTIONS = True
    DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

    REDIS_CACHE_HOST = env("REDIS_CACHE_HOST")
    REDIS_CACHE_PORT = env("REDIS_CACHE_PORT")
    REDIS_CACHE_DB = env("REDIS_CACHE_DB")
    redis_credentials = get_redis_credentials()
    REDIS_USERNAME = redis_credentials.username
    REDIS_PASSWORD = redis_credentials.password

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": f"rediss://{REDIS_USERNAME}@{REDIS_CACHE_HOST}:{REDIS_CACHE_PORT}/{REDIS_CACHE_DB}",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "PARSER_CLASS": "redis.connection._HiredisParser",
                "PASSWORD": REDIS_PASSWORD,
            },
        },
    }
