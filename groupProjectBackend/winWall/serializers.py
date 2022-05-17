## created serializers
from asyncio.windows_events import NULL
from unicodedata import category
from django.forms import ValidationError
from rest_framework import serializers
from .models import StickyNote


class StickyNoteSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    winComment = serializers.CharField(max_length=200)
    guest = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.id')
    ownerName = serializers.ReadOnlyField(source='owner.username')
    # link to winWall  and status
    winWall_id = serializers.IntegerField
    stickyNoteStatus_id = serializers.IntegerField
#    definiing guest based on if owner applied to sticky note 
    def get_guest(self, obj):
        return obj.owner == NULL

    # for sticky notename, would need to make this optional via serializer as well 
    # contributorName = serializers.CharField(max_length=20)
    def create(self, validated_data):
        return StickyNote.objects.create(**validated_data)