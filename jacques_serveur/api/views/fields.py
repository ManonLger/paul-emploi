from rest_framework import viewsets
from rest_framework.response import Response

from api.models.fields import Contract, Location, Language, Interest, Degree, Skill


class FieldsViewSet(viewsets.ViewSet):

    # GET '/api/fields/'
    def list(self, request):
        contract_types_names = [contract.name for contract in list(Contract.objects.all())]
        city_names = [location.city_name for location in list(Location.objects.all())]
        interests_names = [interest.name for interest in list(Interest.objects.all())]
        degrees_names = [degree.name for degree in list(Degree.objects.all())]
        skills_names = [skill.name for skill in list(Skill.objects.all())]
        languages_names = [language.name for language in list(Language.objects.all())]

        resp = {
            'contract_types_names': contract_types_names,
            'city_names': city_names,
            'interests_names': interests_names,
            'degrees_names': degrees_names,
            'skills_names': skills_names,
            'languages_names': languages_names
        }
        return Response(resp)