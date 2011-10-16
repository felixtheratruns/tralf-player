from django.db import models
from datetime import datetime


# Create your models here.
class Player(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __unicode__(self):
        return self.question
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()
    was_published_today.short_description = 'Published today?'
    file_id = models.CharField(max_length=200)
    frame_id_start = models.IntegerField(default=0)
    frame_id_stop = models.IntegerField(default=0)

class Choice(models.Model):
    player = models.ForeignKey(Player)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    def __unicode__(self):
        return self.choice

class Frame(models.Model):
    player = models.ForeignKey(Player)
    frame_text = models.TextField()  
    commit_dtime = models.DateTimeField('date committed')
    line_num_mod = models.IntegerField() 
#    commit_time = models.



