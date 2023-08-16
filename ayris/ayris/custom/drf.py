from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

from ayris.custom.utils import JwtCookieManager
from accounts.authenticate import CustomAuthentication


class CustomSecure:
    permission_classes = (IsAuthenticated,)
    # permission_classes = (permissions.AllowAny,)

    # CHECK if herintence for SessionAuthentication
    # authentication_classes = []
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    authentication_classes = [CustomAuthentication]


class SecureAPIView(APIView, CustomSecure):
    permission_classes = CustomSecure.permission_classes
    authentication_classes = CustomSecure.authentication_classes


class SecureViewSet(viewsets.ModelViewSet, CustomSecure):
    permission_classes = CustomSecure.permission_classes
    authentication_classes = CustomSecure.authentication_classes
