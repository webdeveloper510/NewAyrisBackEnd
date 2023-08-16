from django.conf import settings


class JwtCookieManager:
    @staticmethod
    def set_cookie(response, access_token, refresh_token):
        print("set_cookie")
        print("-------------------")
        response.set_cookie(
            key=settings.SIMPLE_JWT['AUTH_COOKIE'],
            value=access_token,
            expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            # samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        )

        return response

    @staticmethod
    def del_cookie(response, cookies):
        for cookie in cookies:
            print(f"{cookie} cookie deleted")
            response.delete_cookie(cookie)

        return response