# Django settings for utk_hep project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
gettext = lambda s: s
PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    # There are more fields in the generated settings.py, but they are not used
    # if one chooses sqlite3. Feel free to keep them.
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/var/www/utk_hep_web/utk_hep_web.db',
    }
}


MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/admin/'

INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.admin', # Make sure you uncomment this line
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.messages',
        'cms',
        'cms.plugins.text',
        'cms.plugins.picture',
        'cms.plugins.link',
        'cms.plugins.file',
        'cms.plugins.snippet',
        'cms.plugins.googlemap',
        'mptt',
        'publisher',
         'menus',
    )


MIDDLEWARE_CLASSES = (
            'django.middleware.cache.UpdateCacheMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.doc.XViewMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'cms.middleware.page.CurrentPageMiddleware',
        'cms.middleware.user.CurrentUserMiddleware',
            'cms.middleware.toolbar.ToolbarMiddleware',
            'cms.middleware.media.PlaceholderMediaMiddleware',
            'django.middleware.cache.FetchFromCacheMiddleware',
    )

TEMPLATE_DIRS = os.path.join(PROJECT_PATH, 'templates')
    # (templates being the name of my template dir within project-name)
TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.auth',
        'django.core.context_processors.i18n',
        'django.core.context_processors.request',
        'django.core.context_processors.media',
        'cms.context_processors.media',
        )

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-^^nrvi=j9zv!8%7pt7jc3_ln!-9@m#8j+r_=4#stq5-=)ko99'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)


ROOT_URLCONF = 'utk_hep_web.urls'

CMS_TEMPLATES = (
    ('base.html', gettext('default')),
    ('blue2-one.html', gettext('blue2-one')),
    ('blue2-two.html', gettext('blue2-two')),
    ('blue2-three.html', gettext('blue-three')),
)

LANGUAGES = (
        ('en', gettext('English')),
)
