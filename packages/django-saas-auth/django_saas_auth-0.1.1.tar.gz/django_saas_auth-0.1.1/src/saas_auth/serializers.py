from django.contrib.auth import get_user_model
from rest_framework import serializers
from saas_base.drf.serializers import ModelSerializer
from .models import Session, UserProfile, UserToken


class SessionSerializer(serializers.ModelSerializer):
    current_session = serializers.SerializerMethodField()

    class Meta:
        model = Session
        exclude = ('user', 'session_key')

    def get_current_session(self, obj):
        request = self.context['request']
        return request.session.session_key == obj.session_key


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super(UserProfileSerializer, self).create(validated_data)


class UserSerializer(ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = get_user_model()
        exclude = ['password', 'groups', 'user_permissions']
        flatten_fields = ['profile']


class UserTokenSerializer(ModelSerializer):
    class Meta:
        model = UserToken
        exclude = ['user']
        extra_kwargs = {
            'key': {'read_only': True},
            'created_at': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context['request']
        validated_data['user'] = request.user
        return super().create(validated_data)
