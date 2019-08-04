from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.generics import CreateAPIView

from account import permissions
from account.models import Profile
from account.serializers import UserSerializer, AccountSerializer, ProfileSerializer


class CreateUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


def is_email_taken(request):
    model = get_user_model()
    email = request.GET["email"]
    result = ""
    isTaken = model.objects.filter(email=email).exists()
    if isTaken == True:
        result = "true"
    else:
        result = "false"
    return HttpResponse(result)


def is_username_taken(request):
    model = get_user_model()
    username = request.GET["username"]
    result = ""
    isTaken = model.objects.filter(username=username).exists()
    if isTaken == True:
        result = "true"
    else:
        result = "false"
    return HttpResponse(result)


def password_recovery(request):
    model = get_user_model()
    email = request.GET["email"]
    result = ""
    is_registered = model.objects.filter(email=email).exists()
    if is_registered == True:
        new_password = model.objects.make_random_password()

        user_instance = model.objects.get(email=email)
        username = user_instance.username
        user_instance.set_password(new_password)
        user_instance.save()

        msg = "Here is your new password: {0}".format(new_password)
        res = send_mail("Password Recovery", msg, "support@structurecode.com", [email])

        if res == 0:
            result = "false"
        else:
            result = "true"
    else:
        result = "false"
    return HttpResponse(result)


class AccountView(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountSerializer

    def get_queryset(self):
        id = self.request.user.id
        return get_user_model().objects.filter(id=id)


class AccountUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AccountSerializer

    def get_queryset(self):
        id = self.request.user.id
        return get_user_model().objects.filter(id=id)


class ProfileUpdate(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return Profile.objects.filter(user=user)


