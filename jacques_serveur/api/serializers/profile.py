from django.contrib.auth.models import User

from rest_framework import serializers

from api.models.profile import Profile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    desired_location = serializers.SlugRelatedField(slug_field='city_name', read_only=True)
    desired_contract = serializers.SlugRelatedField(slug_field='name', read_only=True)
    interests = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    degrees = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    skills = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    languages = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)

    class Meta:
        model = Profile
        fields = (
            'user',
            'desired_min_salary',
            'desired_max_salary',
            'desired_location',
            'desired_contract',
            'interests',
            'degrees',
            'skills',
            'languages',
        )
