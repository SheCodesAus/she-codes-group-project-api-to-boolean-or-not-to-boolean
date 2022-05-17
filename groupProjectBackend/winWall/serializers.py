from rest_framework import serializers
from .models import WinWall, StickyNote
# from users.models import CustomUser
## created serializers
from asyncio.windows_events import NULL
from unicodedata import category
from django.forms import ValidationError

class WinWallSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    image = serializers.URLField()
    startDate = serializers.DateTimeField()
    endDate = serializers.DateTimeField()
    isOpen = serializers.BooleanField()
    isExported = serializers.BooleanField()
    sticky_Id = serializers.IntegerField()
    user_Id = serializers.ReadOnlyField(source='user.id')
    # auth_id
    collection_Id = serializers.IntegerField()


    def create(self, validated_data):
        return WinWall.objects.create(**validated_data)

class WinWallDetailSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.startDate = validated_data.get('start_date', instance.startDate)
        instance.endDate = validated_data.get('end_date', instance.endDate)
        instance.isOpen = validated_data.get('is_open', instance.isOpen)
        instance.isExported = validated_data.get('is_exported', instance.isExported)
        instance.sticky_Id = validated_data.get('sticky_id', instance.sticky_Id)
        instance.user_Id = validated_data.get('user_id', instance.user_Id)
        # auth_Id
        instance.collection_Id = validated_data.get('collection_id', instance.collection_Id)
        
        instance.save()
        return instance

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
