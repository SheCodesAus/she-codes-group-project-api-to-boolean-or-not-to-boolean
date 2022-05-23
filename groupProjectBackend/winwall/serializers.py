from rest_framework import serializers
from .models import WinWall, StickyNote, Collection
from users.models import SheCodesUser
## created serializers
from datetime import datetime
from django.utils import timezone
# from unicodedata import category
from django.forms import ValidationError

class CollectionSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    image = serializers.URLField()
    is_exported = serializers.BooleanField()
    slug = serializers.SlugField()
    user_id = serializers.ReadOnlyField(source='user_id.id')

    def create(self, validated_data):
        return Collection.objects.create(**validated_data)


class CollectionDetailSerializer(CollectionSerializer):
        
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.is_exported = validated_data.get('is_exported', instance.is_exported)
        instance.slug = validated_data.get('slug', instance.slug)
        
        instance.save() 
        return instance




class StickyNoteSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    win_comment = serializers.CharField(max_length=200)
    # link to owner
    guest = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.id', required=False)
    owner_name = serializers.ReadOnlyField(source='owner.username', required=False)
    
   
    # for sticky notename, would need to make this optional via serializer as well 
    # contributorName = serializers.CharField(max_length=20)

    # link to WinWall  and status
    win_wall_id = serializers.IntegerField()
    # sticky_note_status_id = serializers.IntegerField

    # mthod 2 using a computed status, think this is a better method 
    win_wall_live = serializers.SerializerMethodField()
    # definiing guest based on if owner applied to sticky note 
    def get_win_wall_live(self, obj):
        win_wall_info = WinWall.objects.get(pk=obj.win_wall_id)
        is_live = win_wall_info.is_open()
        if is_live == True:
            return 'Live'
        else:
            return 'Closed'

    def get_guest(self, obj):
        return obj.owner == None

    def create(self, validated_data):
        return StickyNote.objects.create(**validated_data)


class StickyNoteDetailSerializer(StickyNoteSerializer):
    is_approved = serializers.BooleanField(required=False)
    is_archived = serializers.BooleanField(required=False)
    sticky_status = serializers.SerializerMethodField()

    def get_sticky_status(self, obj):
        is_live =  self.get_win_wall_live(obj)
        if is_live == 'Live':
            return 'Live'
        elif is_live == 'Closed' and obj.is_approved == False and obj.is_archived == False:
            return 'Unapproved'
        elif obj.is_approved == True and is_live == 'Closed' and obj.is_archived == False:
            return 'Approved'
        elif obj.is_approved == True and obj.is_archived == True:
            return 'Archived'
        elif obj.is_approved == True and obj.is_archived == False:
            return 'Approved'
        elif obj.is_approved == False and obj.is_archived == False:
            return 'Unapproved'


    def update(self, instance, validated_data):
        instance.win_comment = validated_data.get('win_comment', instance.win_comment)
        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.is_archived = validated_data.get('is_archived', instance.is_archived)
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
    collection_id = serializers.IntegerField()
    owner = serializers.ReadOnlyField(source='owner.id')
    
    # auth_id
    def get_is_open(self, obj):
        return obj.is_open()
    
    def create(self, validated_data):
        return WinWall.objects.create(**validated_data)


# in progress - update all SN via WW 
class WinWallBulkUpdateSerializer(serializers.Serializer):

    # bulk approve or archive sticky notes via the winwall, only as an admin 

    bulk_approve = serializers.BooleanField(required=False)
    bulk_archive = serializers.BooleanField(required=False)


#fixed serializer
class WinWallDetailSerializer(WinWallSerializer):
    stickynotes = StickyNoteSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.is_exported = validated_data.get('is_exported', instance.is_exported)
        instance.owner = validated_data.get('owner', instance.owner)
        # auth_Id
        instance.collection_id = validated_data.get('collection_id', instance.collection_id)
        # instance.sticky_id = validated_data.get('sticky_id', instance.sticky_id)        

        instance.save()
        return instance


