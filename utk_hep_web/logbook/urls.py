from django.conf import settings
from django.conf.urls.defaults import *

from physics_web.logbook.views import *
urlpatterns = patterns('',
    (r'^$',main_page),
    (r'^categories/(\w+)/(.*)',categories),
    (r'^plot_collections/(\w+)/(.*)$',plot_collection),
    
    # Static media
    (r'^repository/(?P<path>.*)$','django.views.static.serve',{'document_root' : settings.UPLOAD_ROOT}),
)