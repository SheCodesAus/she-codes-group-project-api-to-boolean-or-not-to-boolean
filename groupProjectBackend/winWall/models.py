from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

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