from yoza import *
from django.db import models
from datetime import datetime
#filebrowser stuff
from filebrowser.fields import FileBrowseField
from filebrowser.sites import * 
import sys, zipfile, os, os.path
import shutil 
import HTML_CONV
from django.http import HttpResponseRedirect


# Create your models here.
class Player(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
#    def __init__(self, filename):
#        self.file_id = filename
    def __unicode__(self):
        return self.question
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'
    file_name = models.CharField(max_length=200)
    frame_num_start = models.IntegerField(default=0)
    frame_num_stop = models.IntegerField(default=0)

class Choice(models.Model):
    player = models.ForeignKey(Player)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    def __unicode__(self):
        return self.choice

class Frame(models.Model):
    player = models.ForeignKey(Player)
    frame = models.TextField()  
    commit_dtime = models.DateTimeField('date committed')
    line_num_mod = models.IntegerField() 
    def __unicode__(self):
        return self.frame
       
#    results(None,player_id) 
#    commit_time = models.


class Media(models.Model):
    #...
    file = FileBrowseField("File", max_length=200, directory="shells/",  blank=True, 
        null=True,help_text="Upload a video/image/swf, zipped slideshow, etc.")
    #...
    
    def post_upload_callback(sender, **kwargs):
        
 
        if kwargs['file'].extension == ".zip":
            
            thefile = kwargs['file'] 

            # Convert file and dir into absolute paths
            fullpath = os.path.join(settings.MEDIA_ROOT,settings.FILEBROWSER_DIRECTORY,str(thefile))
#            print "full path"+fullpath

            dirname = os.path.dirname(fullpath)
            try:
                # Get a real Python file handle on the uploaded file
                fullpathhandle = open(fullpath, 'r') 
                zfobj = zipfile.ZipFile(fullpathhandle)

#                for el in zfobj.namelist():
#                    print ""
#                    print "element: "+el
#                    elpath = os.path.join(dirname,el)
#                    print "elpath: "+elpath
#                    filedir = os.path.abspath(os.path.join(elpath,os.path.pardir))
#                    #filedir = os.path.splitext(elpath)[0:-1]
#                    print "filedir: "+filedir
#                    if not os.path.exists(filedir):
#                        print "make file dir", filedir
#                        os.makedirs(filedir)
#                    if not os.path.isdir(elpath):
#                        print "extract path "+el+ " "+filedir
#                        zfobj.extract(el,filedir)

                cur_dir = os.getcwd()
                os.chdir(dirname)
                zfobj.extractall()
                os.chdir(cur_dir)

            except:
                e = sys.exc_info()[1] 
                print e
 
            # Now try and delete the uploaded .zip file  
            try:
                os.remove(fullpath)
            except:
                pass
           
            file_path = os.path.splitext(fullpath)[0]
            file_name = os.path.basename(file_path)
            player = Player(question="Do you like "+file_name+" ?",  pub_date=datetime.now(),  file_name=file_name, frame_num_start=0, frame_num_stop=0)
        
            player.save() 
            choice1 = Choice(player=player, choice="like", votes=0)
            choice1.save()
        
            player_id = player.id
            
            try:
                Interface = DjangoInterface(file_path)
            except:
                e = sys.exc_info()[1] 
                print e
           
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
                      
                frame_text = HTML_CONV.plaintext2html(frame_text)
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
            player_id = player.id
            file_dirname = os.path.dirname(file_path)
            folder_path = file_dirname + "/." + file_name + "/"
        
            try:
                os.remove(folder_path)
            except:
                pass
                
    # Signal provided by FileBrowser on every successful upload. 
    FileBrowserSite.filebrowser_post_upload.connect(post_upload_callback)


