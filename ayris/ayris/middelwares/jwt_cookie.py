import json
from django.utils.deprecation import MiddlewareMixin
# from utils import L, LOG   # This logger is custom, you may wish to implement your own or remove it
# from config.settings import JWT_AUTH_REFRESH_COOKIE  # from settings.py
from django.conf import settings
# from ayris.custom.utils import set_cookie

from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken



class JWTRefreshInToCookie(MiddlewareMixin):
    """
    For Django Rest Framework JWT's POST "/token-refresh" endpoint. Check
    for a 'refresh' in the request.COOKIES and if there, move it to the body payload.
    """
    EXCEPT_API_URL = [f"/api/{url}/" for url in ["login", "verify-token", "refresh-token"]]

    print(EXCEPT_API_URL)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        # if request.path == '/api/login/':

        print("process_view")
        print("request.COOKIES", request.COOKIES)

        # check access token is valid
        # with api/verify-token/ and data[token] = access_token
        # OR UntypedToken
        #     then refresh


         # check if token valid or black listed
        # /api/refresh-token/ and data[refresh] = refresh_token

        print(request.path)
        # # IF not login, tokens urls
        # if "access" in request.COOKIES:
        #     access_token = request.COOKIES.get("access")
        #     # raise Exception(token_test[:-1] + "5")
        #     # token_test[-1] = "5"
        #     # token_test = token_test[:-1] + "5"
        #     # CHECK VALID
        #     # # print(UntypedToken(token_test[:-1] + "5"))
        #     # print("****************************")
        #     # print("request.user :", request.user)
        #     # print(access_token)
        #
        #     try:
        #         UntypedToken(access_token)
        #     except (InvalidToken, TokenError) as e:
        #         print(e)
        #     else:
        #         request.META["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        #
        # if "refresh" in request.COOKIES:
        #     refresh_token = request.COOKIES.get("refresh")
        #     print("cHECK REFRESH TOKEN")
        #     try:
        #         token = RefreshToken(refresh_token)
        #     except (InvalidToken, TokenError) as e:
        #         raise Exception(e)
        #     else:
        #         print("refresh token VALID")
        #         print("token : ", token)
        #         print("token : ", token.__dict__)
        #         print("token.access_token : ", str(token.access_token))
        #         access_token = str(token.access_token)
        #         print("-------------------")
        #         print('access_token : ', access_token)
        #         try:
        #             UntypedToken(access_token)
        #         except (InvalidToken, TokenError) as e:
        #             raise Exception(e)
        #         else:
        #             print("ALL GOOD")
        #             request.META["HTTP_AUTHORIZATION"] = "Bearer " + access_token

        # if request.path == '/token/refresh/' and settings.JWT_AUTH_REFRESH_COOKIE in request.COOKIES:
        #     jwt_refresh_cookie = settings.JWT_AUTH_REFRESH_COOKIE
        #     if request.body != b'':
        #         data = json.loads(request.body)
        #         data['refresh'] = request.COOKIES[jwt_refresh_cookie]
        #         request._body = json.dumps(data).encode('utf-8')
        #     else:
        #         print("The incoming request body must be set to an empty objec")
        #         # LOG.info("The incoming request body must be set to an empty object.")

        return None

    # def process_request(self, request):
    #     print("process_request")
    #     return None


