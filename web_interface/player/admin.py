from player.models import Player 
from player.models import Choice
from player.models import Frame
from django.contrib import admin


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2 

class FrameInLine(admin.TabularInline):
    model = Frame
    extra = 1


class PlayerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['question']}),
        ('Date information',{'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline, FrameInLine]
    list_display = ('question', 'pub_date','frame_num_start','frame_num_start', 'was_published_today',)
    list_filter = ['pub_date']    
    search_fields = ['question']
    date_hierarchy = 'pub_date'    
    


admin.site.register(Player, PlayerAdmin)
