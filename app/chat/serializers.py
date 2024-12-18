from django.contrib.auth import get_user_model
from rest_framework import serializers
from chat.models import Message, Room
from django.db import IntegrityError, transaction
from rest_framework.settings import api_settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions


User = get_user_model()


class MessageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Message
        fields = ('text', 'created_at', 'author') 
        read_only_fields = ['created_at', 'author']


class MessageOneToOneSerializer(MessageSerializer): 
    user_to = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta(MessageSerializer.Meta):
        fields = ('text', 'created_at', 'user_to') 
 
    def create(self, validated_data):
        user_to = validated_data.pop('user_to')
        author = validated_data.get('author')
        room = Room.objects.filter(users=author.pk, is_private=True).filter(users=user_to.pk).first()
        if room is None:
            room = Room.objects.create(is_private=True, name=f'{author}&{user_to}_private')
            room.users.set((author, user_to))
        validated_data['room'] = room
        return super().create(validated_data)
    

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'is_private', 'created_at', 'users')
        read_only_fields = ['is_private', 'created_at']
        extra_kwargs = {'users': {'required': False}}

    def save(self, **kwargs):
        request = self.context.get('request')
        self.validated_data.setdefault('users', []) 
        self.validated_data['users'].append(request.user.pk) 
        return super().save(**kwargs)


class UserCreateSerializer(serializers.ModelSerializer):
    """ Created based on Djoser and simplified. """
    
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    default_error_messages = {'error_create': 'Can\'t create user!'}

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + ('username', 'password')

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get('password')
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {'password': serializer_error[api_settings.NON_FIELD_ERRORS_KEY]})
        return attrs

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail('error_create')
        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
        return user


class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'is_active')
        read_only_fields = ['username']

