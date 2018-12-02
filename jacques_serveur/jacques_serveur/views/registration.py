from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.http import require_POST


@require_POST
def register(request):
    body = request.POST
    try:
        email = body['email']
        password = body['password']
    except MultiValueDictKeyError:
        return HttpResponse({'detail': 'You must provide an email and a password.'}, status=400)
    try:
        User.objects.create_user(username=email, email=email, password=password)
    except IntegrityError:
        return HttpResponse({'detail': 'An account with this email already exists.'}, status=400)
    return HttpResponse({'result': 'Success'})
