from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

class WinWall(models.Model):
    title = models.CharField(max_length=200)
    image = models.URLField()
    start_date = models.DateTimeField(default=timezone.now, null = True, blank = True)
    end_date = models.DateTimeField(null = True, blank = True)
    is_open = models.BooleanField()
    is_exported = models.BooleanField()

#   Add FK  
    sticky_id = models.ForeignKey(
        'StickyNotes',on_delete=models.CASCADE,
        related_name='sticky')

    user_id = models.ForeignKey(
        get_user_model(),
        on_delete = models.CASCADE,
        related_name = 'user')

    # auth_id

    collection_id = models.ForeignKey(
        'Collection',on_delete=models.CASCADE,
        related_name='collection')