# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from player.models import Choice, Player

def index(request):
    latest_player_list = Player.objects.all().order_by('-pub_date')[:5]
    return render_to_response('player/index.html', {'latest_player_list': latest_player_list})
    
def detail(request, player_id):
    p = get_object_or_404(Player, pk=player_id)
    return render_to_response('player/detail.html', {'player': p}, context_instance=RequestContext(request))


#def index(request):
#    latest_player_list = Player.objects.all().order_by('-pub_date')[:5]
#    t = loader.get_template('player/index.html')
#    c = Context({
#        'latest_player_list': latest_player_list,
#    })


def results(request, player_id):
    p = get_object_or_404(Player, pk=player_id)
    return render_to_response('player/results.html', {'player': p})


def vote(request, player_id):
    p = get_object_or_404(Player, pk=player_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the player voting form.
        return render_to_response('player/detail.html', {
            'player': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('player_results', args=(p.id,)))

