from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.forms import CharField
from django.conf import settings
from datetime import datetime
from django.utils import timezone
from django.urls import reverse


class Collection(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    is_exported = models.BooleanField()
    # slug = models.SlugField(unique=True, null=True)
    user_id = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        )

    def __str__(self):
        return self.title

class WinWall(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    start_date = models.DateTimeField(default=timezone.now, null = True, blank = True)
    end_date = models.DateTimeField(null = True, blank = True)
    is_exported = models.BooleanField()
    
    def is_open(self):
        today = datetime.now()
        today = timezone.localtime()
        end_time = self.end_date 
        if end_time == None or '':
            end_time = datetime.max()
        
        if end_time > today:
            return True
        else:
            return False

    owner = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        related_name='user_win_walls'
        )

    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE, 
        null = True, 
        blank = True,
        related_name='win_wall_collections'
        )

def get_user_or_anonymous():

    try:
        # return get_user_model()
        print(settings.AUTH_USER_MODEL)
        return settings.AUTH_USER_MODEL
    except ValueError:
        return  'self'
        
class StickyNote(models.Model):
    win_comment = models.CharField(max_length=200)
    is_approved = models.BooleanField(null=True, blank=True)
    is_archived = models.BooleanField(null=True, blank=True)
    # if we wanted to optionally allow users to enter their name as a serpate field on SN :
    # contributorName = models.CharField(max_length=20, blank=True, default='')
    
    # ive called users 'owner' here based on prev project 
    owner = models.ForeignKey(
        get_user_or_anonymous(),
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='owner_stickynotes'
    )
 
    # connection to WinWall 
    win_wall = models.ForeignKey(
        'WinWall',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='stickynotes'
    )

    # connection to status 
    # sticky_note_status = models.ForeignKey(
    #     'sticky_note_status',
    #     null=True, blank=True,
    #     on_delete=models.CASCADE,
    # )
    
class UserAssignment(models.Model):
    # assignment used to override user permissions for specific collection and/or win wall 
    # a single assignment will have a winwall or a collection specified 
    is_admin = models.BooleanField(null=True, blank=True)
    is_approver = models.BooleanField(null=True, blank=True)

    assignee = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    win_wall = models.ForeignKey(
        'WinWall',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='assigned_user'
    )

    collection = models.ForeignKey(
        'Collection',
        on_delete=models.CASCADE, 
        null = True, 
        blank = True,
        related_name='assigned_user'
        )