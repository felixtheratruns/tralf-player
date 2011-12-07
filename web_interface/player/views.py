from django.db import models
import current_player
from yoza import *
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext, Context, loader
from player.models import Choice, Player, Frame
from datetime import datetime, date
import settings
import os.path
import sys

CurrentPlayer = current_player.CurrentPlayer

def index(request):
    latest_player_list = Player.objects.filter(username=request.META['USER']).order_by('-pub_date')
#    latest_player_list = Player.objects.filter(username=request.META['USER']).order_by('-pub_date')[:5]
    return render_to_response('player/index.html', {'latest_player_list': latest_player_list},context_instance=RequestContext(request))
    
def player_detail(request, pk):
    p = get_object_or_404(Player, pk=pk)
    frames = Frame.objects.filter(player=p) 
#    if request.META['USERNAME'] != p.username:
#        return HttpResponseRedirect('/player/')
    return render_to_response('player/player_detail.html', {'player': p, 'frame_list' : frames}, context_instance=RequestContext(request))

def current_player_redirect(request):
    return HttpResponseRedirect("/player/" + str(CurrentPlayer.player_id) + "/")

    
def loadnewplayer(request):
    
    file_name = request.POST['text_ob']
    full_path = os.path.join(settings.MEDIA_ROOT,settings.FILEBROWSER_DIRECTORY,file_name)


    
    player = Player(question="Do you like "+file_name+" ?",  pub_date=datetime.now(),  file_name=file_name, frame_num_start=0, frame_num_stop=0)

    player.save() 
    choice1 = Choice(player=player, choice="like", votes=0)
    choice1.save()

       
    
    print "player save"
    player_id = player.id

#    player = get_object_or_404(Player, pk=player_id)

    Interface = DjangoInterface(full_path)
 #  p = get_object_or_404(player, pk=player_id)

    mode = 1
    u_input = 0
    print_height = 30
    disp = Interface.refresh()

    frame_id_start = None
    frame_id_stop = None
    count = 0
    temp = None
    while disp != None:
        count += 1
        temp = disp
        frame_line = disp[0]
        frame_text = disp[1]
        frame_dtime = disp[2]
        frame_time = disp[3] 
        [year, month, day] = frame_dtime.split('-')
        [hour, minute, second] = frame_time.split(':')

        print "frame dtime:",frame_dtime
        print "frame time:",frame_time
        print "year:",year
        print "month:", month
        print "day:",day
        print "player?",player_id
        frame = Frame(player=player, 
                            line_num_mod=int(frame_line),
                            frame=frame_text,
                            commit_dtime=datetime(int(year), int(month), int(day), int(hour), int(minute), int(second)))

        frame.save()    

        frame_id_stop = frame.id
        if count == 1:
            frame_id_start = frame.id                

        disp = Interface.nFrameButton()
    print "frame start num",frame_id_start
    print "frame stop num",frame_id_stop 
    player.frame_num_start = frame_id_start
    player.frame_num_stop = frame_id_stop

    player.save()
    print "test", player.frame_num_start
    print "test", player.frame_num_stop
    
        #[linenum, frame.stdout.read(), date, time] 
        
#    print "request ",request.POST
#    for key in request.POST.iterkeys():
#        print "key:"+key
#    file_ob = request.FILES['file_ob']    
#    file_name = request.FILES['file_ob'].name
#    print "file name ........"+file_name
#    interface = DjangoInterface(file_ob.temporary_file_path)    
#
#    player = Player.objects.create(question="how is "+file_name+" ?",  pub_date=datetime.now(),  file_name=file_name, frame_num_start=0, frame_num_stop=1)
    return HttpResponseRedirect(reverse('player.views.results', args=(player.id,)))
   


def results(request, pk):
    p = get_object_or_404(Player, pk=pk)
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
        return HttpResponseRedirect(reverse('player.views.results', args=(p.id,)))

