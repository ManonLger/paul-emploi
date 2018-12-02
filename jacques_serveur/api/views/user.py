import json

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from api.serializers.profile import UserSerializer


class UserViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    # POST '/api/users/'
    def create(self, request):
        body = json.loads(request.body.decode())
        try:
            email = body['email']
            password = body['password']
        except MultiValueDictKeyError:
            return Response(
                { 'detail': 'You must provide an email and a password.' },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
        except IntegrityError:
            return Response(
                { 'detail': 'An account with this email already exists.' },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserSerializer(user)
        return Response(serializer.data)
