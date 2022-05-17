# added basic imports to models 

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.forms import CharField


class WinWall(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    startDate = models.DateTimeField(default=timezone.now, null = True, blank = True)
    endDate = models.DateTimeField(null = True, blank = True)
    isOpen = models.BooleanField()
    isExported = models.BooleanField()

#   Add FK  
    sticky_Id = models.ForeignKey(
        'StickyNotes',on_delete=models.CASCADE,
        related_name='sticky')

    user_Id = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        related_name = 'user')

    # auth_Id

    collection_Id = models.ForeignKey(
        'Collection',on_delete=models.CASCADE,
        related_name='collection')


# will need a link to users, winwalls and collections
class StickyNote(models.Model):
    winComment = models.Charfield(max_length=200)
    # if we wanted to optionally allow users to enter their name as a serpate field on SN :
    # contributorName = models.CharField(max_length=20, blank=True, default='')
    
    # ive called users 'owner' here based on prev project 
    owner = models.ForeignKey(
        get_user_model(),
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='owner_stickyNote'
    )
 
    # connection to winWall 
    winWall = models.ForeignKey(
        'winWall',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='StickyNote_id'
    )

    # connection to status 
    stickyNoteStatus = models.ForeignKey(
        'stickyNoteStatus',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='StickyNote_id'
    )
    
