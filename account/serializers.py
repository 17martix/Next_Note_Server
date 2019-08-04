from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers

from account.models import Profile

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = UserModel
        fields = ('id', 'username', 'password', 'email')


class AccountSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='id')
    user_name = serializers.CharField(source='username', required=False)
    password = serializers.CharField(write_only=True, required=False)
    country = serializers.ReadOnlyField(source='profile.country')
    language = serializers.ReadOnlyField(source='profile.language')

    class Meta:
        model = User
        fields = (
        'user_id', 'user_name', 'password', 'email', 'first_name', 'last_name', 'country',
        'language')

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('country', 'language')
