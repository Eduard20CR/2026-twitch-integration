from fastapi import Request

from modules.auth.service.service import AuthService


class AuthController:

    def __init__(self, service: AuthService):
        self.service = service

    async def login(self, request: Request):
        return await self.service.get_login_redirect(request)

    async def callback(self, request: Request):
        return await self.service.handle_callback(request)
