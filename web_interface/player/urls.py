from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView
from player.models import Player




urlpatterns = patterns('',
    (r'^$',
        ListView.as_view(
            queryset=Player.objects.order_by('-pub_date')[:5],
            context_object_name='latest_player_list',
            template_name='player/index.html')),
    (r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Player,
            template_name='player/detail.html')),
    (r'^loadnewplayer/$', 'player.views.loadnewplayer'),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Player,
            template_name='player/results.html'),
        name='player_results'),
    (r'^(?P<player_id>\d+)/vote/$', 'player.views.vote'),

    # Example:
    # (r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

)



