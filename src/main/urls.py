from django.conf.urls.defaults import *
from rpc import router

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^router/$', router, name='router'),
    url(r'^router/api/$', router.api, name='api'),    
)