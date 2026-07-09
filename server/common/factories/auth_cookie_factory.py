from fastapi import Response


class CookieFactory:

    def set_auth_login_cookies(
        self,
        response: Response,
        access_token: str,
        refresh_token: str,
        access_max_age: int,
        refresh_max_age: int,
    ):
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=access_max_age,
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=refresh_max_age,
        )

    def set_auth_refresh_cookies(
        self,
        response: Response,
        access_token: str,
        access_max_age: int,
    ):
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=access_max_age,
        )

    def clear_auth_cookies(self, response: Response):
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
