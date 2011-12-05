from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from player.models import Player




urlpatterns = patterns('player.views',
    url(r'^$', 'index'),
    url(r'^(?P<pk>\d+)/$', 'player_detail'),
    url(r'^loadnewplayer/$', 'loadnewplayer'),
    url(r'^(?P<pk>\d+)/results/$', 'results'),
    url(r'^(?P<player_id>\d+)/vote/$', 'vote'),
    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

)



