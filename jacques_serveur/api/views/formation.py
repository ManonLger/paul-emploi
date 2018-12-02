from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from api.models.formation import Formation
from api.models.profile import AlreadySeenCardException
from api.serializers.formation import FormationSerializer


class FormationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FormationSerializer
    queryset = Formation.objects.all()

    # GET '/api/formation/'
    # Affiche la liste de toutes les formations

    # GET '/api/formation/pk/'
    # Affiche la formation correspondante

    # POST '/api/formation/pk/keep'
    @detail_route(methods=['post'])
    def keep(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            formation = Formation.objects.get(id=pk)
        except Formation.DoesNotExist:
            return Response(
                {'result': 'Error', 'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            request.user.profile.keep_formation(formation)
        except AlreadySeenCardException as exception:
            return Response(
                {'result': 'Error', 'detail': exception.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'result': 'Success'})

    # POST '/api/formation/pk/drop
    @detail_route(methods=['post'])
    def drop(self, request, pk=None):
        if pk is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            formation = Formation.objects.get(id=pk)
        except Formation.DoesNotExist:
            return Response(
                {'result': 'Error', 'detail': 'Not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            request.user.profile.drop_formation(formation)
        except AlreadySeenCardException as exception:
            return Response(
                {'result': 'Error', 'detail': exception.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({'result': 'Success'})
