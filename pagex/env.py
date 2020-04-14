from os import getenv
import environ

env = environ.Env()

# reading .env file
environ.Env.read_env(env_file=getenv('ENV_FILE_NAME', '.env-dev'))

# Email
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_PORT = env('EMAIL_PORT', int, 587)
EMAIL_USE_TLS = env('EMAIL_USE_TLS', bool, True)
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

DATABASES = {
    'default': env.db()
}

ALLOWED_HOSTS = env('ALLOWED_HOSTS', list, default=['*'])
