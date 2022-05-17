# added basic imports to models 

from django.contrib.auth import get_user_model
from django.db import models
from django.forms import CharField

# Create your models here.




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
    