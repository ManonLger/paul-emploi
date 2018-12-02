from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api.models.offer import Offer
from api.models.profile import AlreadySeenCardException
from api.serializers.offer import OfferSerializer, OfferExpandSerializer


class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()

    # GET '/api/offers/'
    # Affiche la liste de toutes les offres

    # GET '/api/offers/pk/'
    # Affiche l'offre correspondante

    # GET '/api/offers/pk/expand/'
    @detail_route(methods=['get'])
    def expand(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            offer = Offer.objects.get(id=pk)
        except Offer.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OfferExpandSerializer(offer)
        return Response(serializer.data)

    # POST '/api/offers/pk/accept/'
    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            offer = Offer.objects.get(id=pk)
        except Offer.DoesNotExist:
            return Response(
                {'result': 'Error', 'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            request.user.profile.accept_offer(offer)
        except AlreadySeenCardException as exception:
            return Response(
                {'result': 'Error', 'detail': exception.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'result': 'Success'})

    # POST '/api/offers/pk/refuse/'
    @detail_route(methods=['post'])
    def refuse(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            offer = Offer.objects.get(id=pk)
        except Offer.DoesNotExist:
            return Response(
                {'result': 'Error', 'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            request.user.profile.refuse_offer(offer)
        except AlreadySeenCardException as exception:
            return Response(
                {'result': 'Error', 'detail': exception.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'result': 'Success'})


# class DegreeDetailView(generics.RetrieveAPIView):
#     serializer_class = DegreeSerializer
#
#     def get_queryset(self):
#         return Degree.objects.all()
#
# class LanguageDetailView(generics.RetrieveAPIView):
#     serializer_class = LanguageSerializer
#
#     def get_queryset(self):
#         return Language.objects.all()
#
# class SkillDetailView(generics.RetrieveAPIView):
#     serializer_class = SkillSerializer
#
#     def get_queryset(self):
#         return Skill.objects.all()
#
# class ContractDetailView(generics.RetrieveAPIView):
#     serializer_class = ContractSerializer
#
#     def get_queryset(self):
#         return Contract.objects.all()
#
# class LocationDetailView(generics.RetrieveAPIView):
#     serializer_class = LocationSerializer
#
#     def get_queryset(self):
#         return Location.objects.all()
#
# class CompanyDetailView(generics.RetrieveAPIView):
#     serializer_class = CompanySerializer
#
#     def get_queryset(self):
#         return Company.objects.all()
