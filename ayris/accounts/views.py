from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from .serializers import RegisterUserSerializer
from ayris.custom.utils import JwtCookieManager
from .authenticate import CustomAuthentication

from ayris.custom.drf import (
SecureAPIView,
SecureViewSet
)
from .models import (
CustomUser,
Profile,
Email,
CustomToken
)
from .serializers import (
UserSerializer,
ProfileSerializer,
EmailSerializer,
MyTokenObtainPairSerializer
)


class UserViewSet(SecureViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class MyUserProfileViewSet(SecureViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return CustomUser.objects.filter(pk=user.id)


class ProfileViewSet(SecureViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
    #
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


class EmailViewSet(SecureViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer


class HelloWorldView(SecureAPIView):

    def get(self, request):
        print("get resquest")

        return Response(
            data={"hello": "world"},
            status=status.HTTP_200_OK
        )


class LogoutAndBlacklistRefreshTokenView(SecureAPIView):

    def post(self, request):
        print(request.user)
        # raise Exception("user : ", request.user)
        # print("request.data", request.data)
        print(request.COOKIES)
        print("refresh_token" in request.COOKIES)
        try:
            if "refresh_token" in request.COOKIES:
                refresh_token = request.COOKIES.get("refresh_token")
                print("refresh_token", refresh_token)
                token = RefreshToken(refresh_token)

                # TODO GET USER FROM REQUEST BY GOOD WAY
                # ADD SOME REAL SECURITY

                payload = token.payload
                payload_user_id = payload.get("user_id")
                request_user = request.user

                if isinstance(request_user, CustomUser) and request_user.id is payload_user_id:

                    try:
                        tok = CustomToken.objects.get(user=payload_user_id)
                    except Exception as e:
                        print("Error :", e)
                        return Response({"ERROR 1"}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        tok.exp = None
                        tok.save()

                        token.blacklist()
                        print("TOKEN BLACKLISTED")

                        # response = redirect('token_obtain_pair')
                        print("request.COOKIES : ", request.COOKIES)
                        response = Response({"DISCONNECT : redirect"}, status=status.HTTP_205_RESET_CONTENT)

                        """
                        MAKE EXPIRE COOKIES
                        """
                        response = JwtCookieManager.del_cookie(response, request.COOKIES)


                        # print("request.COOKIES : ", request.COOKIES)
                        # print("++++++++++++++++++")
                        # print(request.user)
                        logout(request)
                        print("LOGOUT")
                        return response
            else:
                return Response({"Error"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("Error :", e)
            return Response({"CANNOT DISCONNECT"}, status=status.HTTP_400_BAD_REQUEST)


def get_refreh_token_for_user(user):
    return CustomToken.objects.filter(user=user)


def set_refresh_db(user, refresh_token):
    print("FROM set_refresh_db")
    # print(refresh_token.get("jti"))
    print("CREATE A TOKEN")

    try:
        db_token = CustomToken.objects.get(user=user)
        print("USER HAS ALREADY A TOKEN")
    except CustomToken.DoesNotExist:
        db_token = CustomToken()
        db_token.user = user
        print("USER NOT HAS A TOKEN")

    db_token.refresh = str(refresh_token)
    db_token.jti = refresh_token.get("jti")
    db_token.exp = refresh_token.get("exp")
    print(db_token)
    print(db_token.__dict__)
    db_token.save()


def get_tokens_for_user(user):
    print("NEW TOKEN from get_tokens_for_user ")
    # refresh = RefreshToken.for_user(user)
    refresh = MyTokenObtainPairSerializer.get_token(user)
    print(refresh.__dict__)

    set_refresh_db(user, refresh)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class MyLoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, format=None):
        data = request.data
        response = Response()
        print(data)
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(request, email=email, password=password)

        print(user)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)

                login(request, user)
                # SAMESITE
                response = JwtCookieManager.set_cookie(
                    response=response,
                    access_token=data.get("access"),
                    refresh_token=data.get("refresh")
                )

                # response.set_cookie(
                #     key=settings.SIMPLE_JWT['AUTH_COOKIE'],
                #     value=data.get("access"),
                #     expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                #     secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                #     httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                #     # samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
                # )
                #
                # response.set_cookie(
                #     key='refresh_token',
                #     value=data.get("refresh"),
                #     httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                # )

                CSRF = csrf.get_token(request)
                print("CSRF : ", CSRF)

                response.data = {
                    "Success": "Login successfully",
                    "data": data
                }
                return response
            else:
                return Response({"No active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


class CustomUserRegister(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer

    def post(self, request, format='json'):
        serializer = RegisterUserSerializer(data=request.data)
        print("serializer", serializer)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)