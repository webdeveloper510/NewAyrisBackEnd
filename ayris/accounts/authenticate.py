from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings

from rest_framework.authentication import CSRFCheck
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken

def enforce_csrf(request):
    print("from enforce_csrf")
    check = CSRFCheck()
    check.process_request(request)
    print(request.COOKIES)

    reason = check.process_view(request, None, (), {})
    print("reason : ", reason)
    if reason:
        raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

from .models import CustomUser

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("FROM authenticate")
        # print("request :", request)
        # print("request :", request.__dict__)
        # print("request :", request.__dict__.keys())
        # print("request :", request.data)
        header = self.get_header(request)
        print('header : ', header)
        print("COOKIES")
        print(request.COOKIES)
        print(settings.SIMPLE_JWT['AUTH_COOKIE'])
        print("")
        print("request :", request.__dict__)

        print("")
        print("request.data :", request.data)
        print("")
        access_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_COOKIE'])
        # refresh_token = request.COOKIES.get("refresh_token")

        if header is None:
            raw_token = access_token or None
        else:
            raw_token = self.get_raw_token(header)
        
        print("raw token : ", raw_token)
        print("****************")
        if raw_token is None:
            return None
        else:
            try:
                UntypedToken(raw_token)
            except Exception as Error:
                print("Error : ", Error)
        # else:
        #     from ayris.custom.utils import JwtCookieManager
        #     def remake_token_valid(token):
        #         print("")
        #         print("FROM REMAKE TOKEN VALID")
        #         print("")
        #         try:
        #             UntypedToken(token)
        #         except TokenError as e:
        #             print("Error token invalid")
        #             validated_token = RefreshToken(refresh_token)
        #             print(validated_token)
        #             print(validated_token.check_blacklist())
        #
        #             raw_token = str(validated_token.access_token)
        #             new_refresh_token = str(validated_token)
        #             # response = Response()
        #             # JwtCookieManager.set_cookie(response=)
        #             # print("raw_token", raw_token)
        #             # UntypedToken(raw_token)
        #             print("-----------")
        #             return validated_token, True
        #         else:
        #             return None, False
        #
        #     validated_token, is_renew = remake_token_valid(raw_token)
        #
        # print("*****************")
        # print("is_renew : ", is_renew)
        # if not is_renew:
        #     validated_token = self.get_validated_token(raw_token)
        # else:
        #     # RESET A NEW COOKIE
        #     pass

        validated_token = self.get_validated_token(raw_token)

        print("validated_token : ", validated_token)
        print("--------------------------")
        print("request :", request.__dict__.keys())
        print("--------------------------")
        print("validated_token", validated_token)
        """
        TODO find rigth settings to enable
        """
        # enforce_csrf(request)

        return self.get_user(validated_token), validated_token

