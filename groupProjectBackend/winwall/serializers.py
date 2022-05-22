from rest_framework import serializers
from .models import WinWall, StickyNote
from users.models import SheCodesUser
## created serializers
from datetime import datetime
from django.utils import timezone
from unicodedata import category
from django.forms import ValidationError




class StickyNoteSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    win_comment = serializers.CharField(max_length=200)
    guest = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.id', required=False)
    owner_name = serializers.ReadOnlyField(source='owner.username', required=False)
    is_approved = serializers.BooleanField()
    is_archived = serializers.BooleanField()
   

    # link to WinWall  and status
    win_wall_id = serializers.IntegerField()
    # sticky_note_status_id = serializers.IntegerField

    # mthod 2 using a computed status, think this is a better method 

    sticky_status = serializers.SerializerMethodField()

    # definiing guest based on if owner applied to sticky note 
    def sticky_status(self, obj):
        win_wall_info = WinWall.objects.filter(pk=obj.win_wall_id)
        is_live = win_wall_info.is_open()
        if is_live == True:
            return 'Live'

        return

    def get_guest(self, obj):
        return obj.owner == None

    # for sticky notename, would need to make this optional via serializer as well 
    # contributorName = serializers.CharField(max_length=20)
    def create(self, validated_data):
        return StickyNote.objects.create(**validated_data)


class StickyNoteDetailSerializer(StickyNoteSerializer):

    def update(self, instance, validated_data):
        instance.win_comment = validated_data.get('win_comment', instance.win_comment)
        instance.save()
        return instance 


class WinWallSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    image = serializers.URLField()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    is_open = serializers.SerializerMethodField()
    is_exported = serializers.BooleanField()
    # sticky_id = serializers.IntegerField()
    # user_id = serializers.ReadOnlyField(source='user.id')
    owner = serializers.ReadOnlyField(source='owner.id')
    
    # auth_id
    # collection_id = serializers.IntegerField()
    def get_is_open(self, obj):
        return obj.is_open()
        
    def create(self, validated_data):
        return WinWall.objects.create(**validated_data)


class WinWallBulkUpdateSerializer(serializers.Serializer):
    # bulk_approve = serializers.BooleanField()
    # bulk_archive = serializers.BooleanField()

    #  nice to have - add sum of approved or archived sticky notes 
    def update(self, instance, validated_data):
        for note in instance:
            note.is_approved = validated_data.get('bulk_approve', note.is_approved)
            note.is_archived = validated_data.get('bulk_archive', note.is_archived)
            note.save()
        return instance


#fixed serializer
class WinWallDetailSerializer(WinWallSerializer):
    stickynotes = StickyNoteSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.is_exported = validated_data.get('is_exported', instance.is_exported)
        # instance.sticky_id = validated_data.get('sticky_id', instance.sticky_id)
        instance.owner = validated_data.get('owner', instance.owner)
        # auth_Id
        # instance.collection_id = validated_data.get('collection_id', instance.collection_id)
        
        instance.save()
        return instance


