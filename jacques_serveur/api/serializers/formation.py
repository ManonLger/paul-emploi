from rest_framework import serializers

from api.models.formation import Formation
from api.serializers.fields import DegreeSerializer, SkillSerializer, LocationSerializer


class FormationSerializer(serializers.ModelSerializer):
    required_skills = SkillSerializer(many=True, read_only=True)
    acquired_skills = SkillSerializer(many=True, read_only=True)
    required_degrees = DegreeSerializer(many=True, read_only=True)
    acquired_degree = DegreeSerializer(read_only=True)
    location = serializers.SlugRelatedField(slug_field='city_name', read_only=True)
    language = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Formation
        fields = '__all__'


class FormationIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Formation
        fields = ('id',)
