DJANGO_APPS = [

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

EXTERNAL_APPS = [

    "rest_framework",
    "django_filters"

]

LOCAL_APPS = [
    'accounts.apps.AccountsConfig',
    'products.apps.ProductsConfig',
    'categories.apps.CategoriesConfig',

]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + LOCAL_APPS
