from django.forms import CharField
from rest_framework import serializers
from .models import SheCodesUser, SheCodesGuestUser
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class SheCodesGuestUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()

    def create(self, validated_data):
        return SheCodesGuestUser.objects.create(**validated_data)

class SheCodesUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    username = serializers.CharField(max_length=200)
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=SheCodesUser.objects.all())]
        )
    avatar = serializers.URLField()
    bio = serializers.CharField(max_length=600)
    social_link = serializers.URLField()

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = SheCodesUser
        fields = ('id', 'username', 'password', 'password2', 'email', 'first_name', 'last_name', 'avatar', 'bio', 'social_link')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = SheCodesUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data['avatar'],
            bio=validated_data['bio'],
            social_link=validated_data['social_link']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user

class ViewSheCodesUserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(max_length=40)
    last_name = serializers.CharField(max_length=40)
    username = serializers.CharField(max_length=60)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=SheCodesUser.objects.all())]
        )
    avatar = serializers.URLField()
    bio = serializers.CharField(max_length=600)
    social_link = serializers.URLField()

    def create(self, validated_data):
        return SheCodesUser.objects.create(**validated_data)

class SheCodesUserDetailSerializer(ViewSheCodesUserSerializer):
        def update(self, instance, validated_data):
            instance.username = validated_data.get('username',instance.username)
            instance.first_name = validated_data.get('first_name',instance.first_name)
            instance.last_name = validated_data.get('last_name',instance.last_name)
            instance.email = validated_data.get('email',instance.email)
            instance.avatar = validated_data.get('avatar', instance.avatar)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.social_link = validated_data.get('social_link', instance.social_link)
            instance.save()
            return instance
