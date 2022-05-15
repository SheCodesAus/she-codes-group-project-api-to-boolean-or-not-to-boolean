from rest_framework import serializers
from .models import WinWall
# from users.models import CustomUser

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
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.is_exported = validated_data.get('is_exported', instance.is_exported)
        instance.sticky_id = validated_data.get('sticky_id', instance.sticky_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        # auth_id
        instance.collection_id = validated_data.get('collection', instance.collection)
        instance.save()
        return instance
