from fastapi import Request, Response

from modules.auth.services.auth_service import AuthService
from common.factories.auh_redirect_factory import RedirectFactory
from common.factories.auth_cookie_factory import CookieFactory


class AuthController:

    def __init__(
        self, service: AuthService, redirect_factory: RedirectFactory, cookie_factory: CookieFactory, frontend_url: str
    ):
        self.service = service
        self.redirect_factory = redirect_factory
        self.cookie_factory = cookie_factory
        self.frontend_url = frontend_url

    async def login(self, request: Request):
        return await self.service.get_login_redirect(request)

    async def callback(self, request: Request):

        auth_result = await self.service.handle_callback(request)

        response = self.redirect_factory.to_frontend(self.frontend_url)

        self.cookie_factory.set_auth_login_cookies(
            response=response,
            access_token=auth_result.jwt_access_token,
            refresh_token=auth_result.jwt_refresh_token,
            access_max_age=auth_result.access_expires_in,
            refresh_max_age=auth_result.refresh_expires_in,
        )

        return response

    async def refresh(self, refresh_token: str):
        try:
            auth_result = await self.service.refresh_tokens(refresh_token)

            response = Response()

            self.cookie_factory.set_auth_refresh_cookies(
                response=response,
                access_token=auth_result.jwt_access_token,
                access_max_age=auth_result.access_expires_in,
            )

            return response
        except Exception as e:
            raise e
