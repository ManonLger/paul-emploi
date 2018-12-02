from rest_framework import serializers

from api.models.offer import Offer, Company
from api.serializers.fields import LocationSerializer, DegreeSerializer, SkillSerializer, LanguageSerializer


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(read_only=True, slug_field='name')
    languages = LanguageSerializer(many=True, read_only=True)
    location = serializers.SlugRelatedField(read_only=True, slug_field='city_name')
    degrees = DegreeSerializer(many=True, read_only=True)
    contract_type = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Offer
        fields = ('title',
                'company',
                'languages',
                'location',
                'degrees',
                'min_salary',
                'max_salary',
                'contract_type',
                'creation_date')


class OfferIdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        fields = ('id',)


class OfferExpandSerializer(OfferSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    company = CompanySerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = ('title',
                  'company',
                  'languages',
                  'location',
                  'degrees',
                  'min_salary',
                  'max_salary',
                  'contract_type',
                  'creation_date',
                  'skills',
                  'description',
                  'weekly_work_time',
                  'experience_name')
