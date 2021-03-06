from rest_framework import serializers
from .models import WinWall, StickyNote, Collection, UserAssignment
from users.models import SheCodesUser

class CollectionSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(max_length=200)
    image = serializers.URLField()
    is_exported = serializers.BooleanField()
    # slug = serializers.SlugField()
    user_id = serializers.ReadOnlyField(source='user_id.id')

    def create(self, validated_data):
        return Collection.objects.create(**validated_data)


class StickyNoteSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    win_comment = serializers.CharField(max_length=200)
    # link to owner
    guest = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.id', required=False)
    owner_name = serializers.ReadOnlyField(source='owner.username', required=False)

    # link to WinWall  and status
    win_wall_id = serializers.IntegerField()

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

    def is_false_or_none(self, bool):
        return bool == False or bool == None

    def compute_status(self,obj):
        is_live =  self.get_win_wall_live(obj)
        if is_live == 'Live':
            return 'Live'
        elif is_live == 'Closed' and self.is_false_or_none(obj.is_approved) and self.is_false_or_none(obj.is_archived):
            return 'Unapproved'
        elif obj.is_approved == True and is_live == 'Closed' and self.is_false_or_none(obj.is_archived):
            return 'Approved'
        elif obj.is_approved == True and obj.is_archived == True:
            return 'Archived'
        elif self.is_false_or_none(obj.is_approved) and obj.is_archived == True:
            return 'Archived'
        elif obj.is_approved == True and self.is_false_or_none(obj.is_archived):
            return 'Approved'
        else:
            return 'Unapproved'

class StickyNoteDetailSerializer(StickyNoteSerializer):
    sticky_status = serializers.SerializerMethodField()

    def get_sticky_status(self, obj):
        return self.compute_status(obj)

    def update(self, instance, validated_data):
        instance.win_comment = validated_data.get('win_comment', instance.win_comment)
        instance.save()
        return instance 

class AdminStickyNoteDetailSerializer(StickyNoteSerializer):
    is_approved = serializers.BooleanField(required=False)
    is_archived = serializers.BooleanField(required=False)
    sticky_status = serializers.SerializerMethodField()
    def get_sticky_status(self, obj):
        return self.compute_status(obj)


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
    collection_id = serializers.IntegerField()
    owner = serializers.ReadOnlyField(source='owner.id')

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
    stickynotes = serializers.SerializerMethodField() 
    
    # fix to make stickynotes order correctly after update 

    def get_stickynotes(self,obj):
        notes = obj.stickynotes.order_by('id')
        return StickyNoteDetailSerializer(notes,many = True).data

    def update(self, instance, validated_data):
        
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.is_exported = validated_data.get('is_exported', instance.is_exported)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance

class CollectionDetailSerializer(CollectionSerializer):
    win_wall_collections = WinWallSerializer(many=True, read_only=True)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.is_exported = validated_data.get('is_exported', instance.is_exported)
        instance.save() 
        return instance
        
class UserAssignmentsSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    is_admin = serializers.BooleanField(required=False)
    is_approver = serializers.BooleanField(required=False)
    assignee_id = serializers.IntegerField()
    win_wall_id = serializers.IntegerField(required=False)
    collection_id = serializers.IntegerField(required=False)
    def create(self, validated_data):
        return UserAssignment.objects.create(**validated_data)

class UserAssignmentsDetailSerializer(UserAssignmentsSerializer):
    def update(self, instance, validated_data):
        instance.is_admin = validated_data.get('is_admin', instance.is_admin)
        instance.is_approver = validated_data.get('is_approver', instance.is_approver)
        instance.assignee_id = validated_data.get('assignee_id', instance.assignee_id)
        instance.win_wall_id = validated_data.get('win_wall_id', instance.win_wall_id)
        instance.collection_id = validated_data.get('collection_id', instance.collection_id)
        instance.save()
        return instance