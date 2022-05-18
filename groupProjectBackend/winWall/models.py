# added basic imports to models 

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.forms import CharField


class WinWall(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    start_date = models.DateTimeField(default=timezone.now, null = True, blank = True)
    end_date = models.DateTimeField(null = True, blank = True)
    is_open = models.BooleanField()
    is_exported = models.BooleanField()

#   Add FK  
    # sticky_note = models.ForeignKey(
    #     'StickyNote',on_delete=models.CASCADE,
    #     )

    user_id = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        )

    # auth_Id

    # collection_id = models.ForeignKey(
    #     'collection',on_delete=models.CASCADE,
    #     )


# will need a link to users, winwalls and collections
class StickyNote(models.Model):
    win_comment = models.CharField(max_length=200)
    # if we wanted to optionally allow users to enter their name as a serpate field on SN :
    # contributorName = models.CharField(max_length=20, blank=True, default='')
    
    # ive called users 'owner' here based on prev project 
    owner = models.ForeignKey(
        get_user_model(),
        null=True, blank=True,
        on_delete=models.CASCADE,
    )
 
    # connection to WinWall 
    win_wall = models.ForeignKey(
        'WinWall',
        null=True, blank=True,
        on_delete=models.CASCADE,
    )

    # connection to status 
    # sticky_note_status = models.ForeignKey(
    #     'sticky_note_status',
    #     null=True, blank=True,
    #     on_delete=models.CASCADE,
    # )
    
