import json

from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response

from api.models.fields import Contract, Location, Interest, Degree, Skill, Language
from api.models.profile import Profile
from api.serializers.formation import FormationIdSerializer
from api.serializers.offer import OfferIdSerializer
from api.serializers.profile import ProfileSerializer


class ProfileViewSet(viewsets.ViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    # GET '/api/profile/'
    def list(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({ 'detail': 'Profile not found.' }, status=status.HTTP_404_NOT_FOUND)
        return Response(self.serializer_class(profile).data)

    # PUT '/api/profile/'
    def put(self, request):
        try:
            profile = request.user.profile
            body = json.loads(request.body.decode())
        except Profile.DoesNotExist:
            return Response({ 'detail': 'Profile not found.' }, status=status.HTTP_404_NOT_FOUND)

        try:
            profile.desired_location = Location.objects.get(city_name=body['desired_location'])
        except KeyError:
            pass
        except Location.DoesNotExist:
            return Response(
                { 'detail': 'Please enter a valid city name. See http://germoon.nebulae.co/api/fields for more info.' },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            profile.desired_contract = Contract.objects.get(name=body['desired_contract'])
        except KeyError:
            pass
        except Contract.DoesNotExist:
            return Response(
                { 'detail': 'Please enter a valid contract type. See http://germoon.nebulae.co/api/fields for more info. '},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            items_list = body['interests']
            profile.interests = Interest.objects.none()
            for item in items_list:
                try:
                    item = Interest.objects.get(name=item)
                    profile.interests.add(item)
                except Interest.DoesNotExist:
                    return Response(
                        { 'detail': 'Please enter valid interests. See http://germoon.nebulae.co/api/fields for more info. '},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except KeyError:
            pass

        try:
            items_list = body['degrees']
            profile.degrees = Degree.objects.none()
            for item in items_list:
                try:
                    item = Degree.objects.get(name=item)
                    profile.degrees.add(item)
                except Degree.DoesNotExist:
                    return Response(
                        {'detail': 'Please enter valid degrees. See http://germoon.nebulae.co/api/fields for more info. '},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except KeyError:
            pass

        try:
            items_list = body['skills']
            profile.skills = Skill.objects.none()
            for item in items_list:
                try:
                    item = Skill.objects.get(name=item)
                    profile.skills.add(item)
                except Skill.DoesNotExist:
                    return Response(
                        {'detail': 'Please enter valid skills. See http://germoon.nebulae.co/api/fields for more info. '},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except KeyError:
            pass

        try:
            items_list = body['languages']
            profile.languages = Language.objects.none()
            for item in items_list:
                try:
                    item = Language.objects.get(name=item)
                    profile.languages.add(item)
                except Language.DoesNotExist:
                    return Response(
                        {'detail': 'Please enter valid languages. See http://germoon.nebulae.co/api/fields for more info. '},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        except KeyError:
            pass

        try:
            if isinstance(body['desired_min_salary'], int):
                profile.desired_min_salary = body['desired_min_salary']
        except KeyError:
            pass

        try:
            if isinstance(body['desired_max_salary'], int):
                profile.desired_max_salary = body['desired_max_salary']
        except KeyError:
            pass

        profile.save()
        return Response(self.serializer_class(profile).data)

    # GET '/api/profile/accepted_offers/'
    @list_route(methods=['get'])
    def accepted_offers(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        accepted_offers = profile.accepted_offers
        serializer = OfferIdSerializer(accepted_offers, many=True)
        return Response(serializer.data)

    # GET '/api/profile/offers_to_show/'
    @list_route(methods=['get'])
    def offers_to_show(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        offers_to_show = profile.offers_to_show
        return Response(offers_to_show)

    # GET '/api/profile/kept_formations/'
    @list_route(methods=['get'])
    def kept_formations(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        kept_formations = profile.kept_formations
        serializer = FormationIdSerializer(kept_formations, many=True)
        return Response(serializer.data)

    # GET '/api/profile/formations_to_show/'
    @list_route(methods=['get'])
    def formations_to_show(self, request):
        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        formations_to_show = profile.formations_to_show
        return Response(formations_to_show)
