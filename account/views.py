import json

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions

from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema

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


@csrf_exempt
def password_recovery(request):
    result = "false"
    if request.body:
        data = json.loads(request.body)
        for account in data:
            model = get_user_model()
            email = account['email']
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


class CustomObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer
    if coreapi is not None and coreschema is not None:
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        # account=get_user_model().objects.get(id=user.id)
        profile=Profile.objects.get(user=user)
        token, created = Token.objects.get_or_create(user=user)
        content = {
            'token': token.key,
            'user_id': user.id,
            'uname': user.username,
            'email': user.email,
            'language':profile.language,
            'archive_task':profile.done_todo_delay,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return Response(content)
