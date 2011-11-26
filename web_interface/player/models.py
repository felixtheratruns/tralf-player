from django.db import models
from datetime import datetime
#filebrowser stuff
from filebrowser.fields import FileBrowseField
from filebrowser.sites import * 
import sys, zipfile, os, os.path
import shutil
 


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
       
class Media(models.Model):
    #...
    file = FileBrowseField("File", max_length=200, directory="shells/",  blank=True, 
        null=True,help_text="Upload a video/image/swf, zipped slideshow, etc.")
    #...
    
        
    def post_upload_callback(sender, **kwargs):
        """
        Signal receiver called each time an upload has finished.
        Triggered by Filebrowser's filebrowser_post_upload signal:
        http://code.google.com/p/django-filebrowser/wiki/signals .
        We'll use this to unzip .zip files in place when/if they're uploaded.
        """

        if kwargs['file'].extension == ".zip":
            # Note: this doesn't test for corrupt zip files. 
            # If encountered, user will get an HTTP Error 
            # and file will remain on the server.

            # We get returned relative path names from Filebrowser
            path = kwargs['path'] 
            thefile = kwargs['file'] 
            
            # Convert file and dir into absolute paths
            fullpath = os.path.join(settings.MEDIA_ROOT,thefile.path_relative)
            dirname = os.path.dirname(fullpath)
            
            # Get a real Python file handle on the uploaded file
            fullpathhandle = open(fullpath, 'r') 

            # Unzip the file, creating subdirectories as needed
            zfobj = zipfile.ZipFile(fullpathhandle)
            for name in zfobj.namelist():
                if name.endswith('/'):
                    try: # Don't try to create a directory if exists
                        os.mkdir(os.path.join(dirname, name))
                    except:
                        pass
                else:
                    outfile = open(os.path.join(dirname, name), 'wb')
                    outfile.write(zfobj.read(name))
                    outfile.close()
                
            # Now try and delete the uploaded .zip file and the 
            # stub __MACOSX dir if they exist.
            try:
                os.remove(fullpath)
            except:
                pass
                
            try:
                osxjunk = os.path.join(dirname,'__MACOSX')
                shutil.rmtree(osxjunk)
            except:
                pass                
            
    # Signal provided by FileBrowser on every successful upload. 
    FileBrowserSite.filebrowser_post_upload.connect(post_upload_callback)

#    commit_time = models.



