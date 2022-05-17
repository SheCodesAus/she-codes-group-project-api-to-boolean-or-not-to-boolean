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
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    is_open = serializers.BooleanField()
    is_exported = serializers.BooleanField()
    sticky_id = serializers.IntegerField()
    user_id = serializers.ReadOnlyField(source='user.id')
    # auth_id
    collection_id = serializers.IntegerField()


    def create(self, validated_data):
        return WinWall.objects.create(**validated_data)

class WinWallDetailSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.isOpen = validated_data.get('is_open', instance.isOpen)
        instance.is_exported = validated_data.get('is_exported', instance.is_exported)
        instance.sticky_id = validated_data.get('sticky_id', instance.sticky_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        # auth_Id
        instance.collection_id = validated_data.get('collection_id', instance.collection_id)
        
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
