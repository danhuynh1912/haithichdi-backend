from functools import lru_cache
from pathlib import Path
import os
from urllib.parse import urlparse

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def get_bool_env(name: str, default: str = "0") -> bool:
    return os.environ.get(name, default).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def get_required_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ImproperlyConfigured(f"{name} must be set")
    return value


@lru_cache(maxsize=1)
def get_ssm_client():
    region_name = (
        os.environ.get("AWS_REGION", "").strip()
        or os.environ.get("AWS_DEFAULT_REGION", "").strip()
        or None
    )
    return boto3.client(
        "ssm",
        region_name=region_name,
        config=Config(
            connect_timeout=2,
            read_timeout=5,
            retries={
                "max_attempts": 2,
                "mode": "standard",
            },
        ),
    )


@lru_cache(maxsize=32)
def get_ssm_parameter(name: str) -> str:
    print(f"Loading SSM parameter {name}", flush=True)
    try:
        response = get_ssm_client().get_parameter(
            Name=name,
            WithDecryption=True,
        )
    except (BotoCoreError, ClientError) as exc:
        print(f"Unable to read SSM parameter {name}: {exc}", flush=True)
        raise ImproperlyConfigured(
            f"Unable to read SSM parameter {name}"
        ) from exc

    value = response["Parameter"]["Value"].strip()
    if not value:
        raise ImproperlyConfigured(f"SSM parameter {name} is empty")
    print(f"Loaded SSM parameter {name}", flush=True)
    return value


def get_secret_env(name: str, default: str | None = None) -> str:
    value = os.environ.get(name, "").strip()
    if value:
        return value

    parameter_name = os.environ.get(f"{name}_SSM_PARAMETER", "").strip()
    if parameter_name:
        return get_ssm_parameter(parameter_name)

    if default is not None:
        return default

    raise ImproperlyConfigured(
        f"{name} must be set directly or via {name}_SSM_PARAMETER"
    )


def normalize_domain_or_url(value: str | None) -> str | None:
    if not value:
        return None

    normalized = value.strip()
    if not normalized:
        return None

    parsed = urlparse(normalized if "://" in normalized else f"https://{normalized}")
    host = parsed.netloc or parsed.path
    path = parsed.path if parsed.netloc else ""
    path = path.rstrip("/")

    return f"{host}{path}" if path else host


def infer_url_protocol(value: str | None, default: str = "https:") -> str:
    if not value:
        return default

    parsed = urlparse(value if "://" in value else f"{default}//{value}")
    return f"{parsed.scheme}:" if parsed.scheme else default

SECRET_KEY = get_secret_env("DJANGO_SECRET_KEY", default="dev-secret-key")
DEBUG = get_bool_env("DJANGO_DEBUG")

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "corsheaders",
    "rest_framework",
    "storages",
    "accounts",
    "tours",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"
ASGI_APPLICATION = "backend.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "tours_db"),
        "USER": os.environ.get("POSTGRES_USER", "tours_user"),
        "PASSWORD": get_secret_env("POSTGRES_PASSWORD", default="tours_pass"),
        "HOST": os.environ.get("POSTGRES_HOST", "db"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

AUTH_USER_MODEL = "accounts.User"

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
]

USE_S3 = get_bool_env("USE_S3")
if USE_S3:
    AWS_STORAGE_BUCKET_NAME = get_required_env("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "us-east-1")
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL", "").strip() or None

    # Production should use a CloudFront host or media domain here.
    # Local MinIO can still use AWS_S3_PUBLIC_ENDPOINT_URL for path-style URLs.
    AWS_S3_CUSTOM_DOMAIN = normalize_domain_or_url(
        os.environ.get("AWS_S3_CUSTOM_DOMAIN")
    )

    if not AWS_S3_CUSTOM_DOMAIN:
        public_base_url = (
            os.environ.get("AWS_S3_PUBLIC_BASE_URL", "").strip()
            or os.environ.get("AWS_S3_PUBLIC_ENDPOINT_URL", "").strip()
        )
        public_host = normalize_domain_or_url(public_base_url)
        if public_host:
            AWS_S3_CUSTOM_DOMAIN = (
                f"{public_host}/{AWS_STORAGE_BUCKET_NAME}"
                if AWS_S3_ENDPOINT_URL
                else public_host
            )

    storage_options = {
        "bucket_name": AWS_STORAGE_BUCKET_NAME,
        "region_name": AWS_S3_REGION_NAME,
        "default_acl": None,
        "file_overwrite": False,
        "querystring_auth": False,
    }

    provided_access_key = os.environ.get("AWS_ACCESS_KEY_ID", "").strip()
    provided_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "").strip()
    if provided_access_key and provided_secret_key:
        storage_options["access_key"] = provided_access_key
        storage_options["secret_key"] = provided_secret_key

    if AWS_S3_ENDPOINT_URL:
        storage_options["endpoint_url"] = AWS_S3_ENDPOINT_URL
        storage_options["addressing_style"] = os.environ.get(
            "AWS_S3_ADDRESSING_STYLE", "path"
        )

    if AWS_S3_CUSTOM_DOMAIN:
        storage_options["custom_domain"] = AWS_S3_CUSTOM_DOMAIN
        storage_options["url_protocol"] = infer_url_protocol(
            os.environ.get("AWS_S3_PUBLIC_BASE_URL")
            or os.environ.get("AWS_S3_PUBLIC_ENDPOINT_URL")
        )

    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": storage_options,
    }
