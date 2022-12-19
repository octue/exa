import os
import sys
import environ


env = environ.Env()


def get_db_conf():
    """
    Configures database for postgres from a URL if supplied, otherwise
    from the default used with the devcontainer
    """
    print(env.str("DATABASE_URL", default=""))
    if len(env.str("DATABASE_URL", default="")) > 0:
        return env.db("DATABASE_URL")
    return {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "postgres_db",
        "USER": "postgres_user",
        "PASSWORD": "postgres_password",
        "HOST": "localhost",
        "PORT": "5432",
    }


# -----------------------------------------------------------
# TERRAFORM VARIABLES USED FOR CONSTRUCTION OF RESOURCE NAMES
# -----------------------------------------------------------
TERRAFORM_PROJECT_NAME = "octue-exa"  # 'my-exa-project' in the documentation
TERRAFORM_RESOURCE_AFFIX = "exa"  # 'my-exa-project' in the documentation
TERRAFORM_ENVIRONMENT = "main"  # Typically we use a slugified branch name for this
TERRAFORM_REGION = "europe-west1"


# ---------------------------------------------------------------------------
# GENERIC DJANGO SETTINGS FOR THE TEST APP
# ---------------------------------------------------------------------------

DEBUG = True


# Add the backend directory to the system path so django can find the apps without renaming them to e.g. server.example
# (from https://stackoverflow.com/questions/3948356/how-to-keep-all-my-django-applications-in-specific-folder)
SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SERVER_DIR)


INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.admin",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "django_extensions",  # Gives us shell_plus and reset_db for manipulating the test server
    "django_gcp.apps.DjangoGCPAppConfig",
    "django_twined",
    "example.apps.ExampleAppConfig",
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(SERVER_DIR, "example", "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ALLOWED_HOSTS = [
    "localhost",
    ".loca.lt",
]  # Adding loca.lt allows developers to expose the example server using localtunnel

DATABASES = {"default": get_db_conf()}

ROOT_URLCONF = "server.urls"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

SECRET_KEY = "secretkey"

# ASGI_APPLICATION = "server.asgi:application"


# ---------------------------------------------------------------------------
# HERE'S HOW TO SET UP STATIC AND MEDIA STORAGE
# ---------------------------------------------------------------------------

# MEDIA FILES
DEFAULT_FILE_STORAGE = "django_gcp.storage.GoogleCloudMediaStorage"
GCP_STORAGE_MEDIA = {"bucket_name": f"{TERRAFORM_RESOURCE_AFFIX}-{TERRAFORM_ENVIRONMENT}-assets-media"}
MEDIA_URL = f"https://storage.googleapis.com/{GCP_STORAGE_MEDIA['bucket_name']}/"
MEDIA_ROOT = "/media/"

# STATIC FILES
STATICFILES_STORAGE = "django_gcp.storage.GoogleCloudStaticStorage"
GCP_STORAGE_STATIC = {"bucket_name": f"{TERRAFORM_RESOURCE_AFFIX}-{TERRAFORM_ENVIRONMENT}-assets-static"}
STATIC_URL = f"https://storage.googleapis.com/{GCP_STORAGE_STATIC['bucket_name']}/"
STATIC_ROOT = "/static/"


# ---------------------------------------------------------------------------
# HERE'S HOW TO SET UP TASKS
# ---------------------------------------------------------------------------

GCP_TASKS_DEFAULT_QUEUE_NAME = f"{TERRAFORM_RESOURCE_AFFIX}-{TERRAFORM_ENVIRONMENT}-primary"
GCP_TASKS_DELIMITER = "--"
# This is the domain on which the worker app can receive requests
# You can use localtunnel to easily create your own public domain to
# run end-to-end integration tests with a real GCP project
GCP_TASKS_DOMAIN = "https://outrageous-horny-giraffe.loca.lt"
GCP_TASKS_EAGER_EXECUTE = False
GCP_TASKS_REGION = TERRAFORM_REGION
GCP_TASKS_RESOURCE_AFFIX = f"{TERRAFORM_RESOURCE_AFFIX}-{TERRAFORM_ENVIRONMENT}"


# client = google.cloud.storage.Client()
# gcs_bucket = client.get_bucket(GCP_STORAGE_MEDIA["bucket_name"])
# ddcu_bucket_identifier = register_gcs_bucket(gcs_bucket)


# DJANGO TWINED
TWINED_BASE_URL = GCP_TASKS_DOMAIN  # The base url to which ServiceUsageEvents get pushed when services are running. You typically want this to be a worker URL, to consume the event stream.
TWINED_DEFAULT_NAMESPACE = TERRAFORM_PROJECT_NAME
TWINED_DEFAULT_TAG = "latest"
