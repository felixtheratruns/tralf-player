from django.db import models
from datetime import datetime


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



#    commit_time = models.



