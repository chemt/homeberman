from django.conf.urls.defaults import *
from rpc import router

urlpatterns = patterns('main.views',
    url(r'^$', 'index', name='index'),
    url(r'^add_game', 'add_game', name='add_game'),
    url(r'^join/(?P<id>\d+)/$', 'join_game', name='join_game'),
    url(r'^finished/(?P<game_id>\d+)/$', 'finished', name='finished'),
    url(r'^games_history/$', 'games_history', name='games_history'),
    url(r'^list_games/$', 'list_games', name='list_games'),
    url(r'^router/$', router, name='router'),
    url(r'^router/api/$', router.api, name='api'),    
)
