from fastapi.responses import RedirectResponse


class RedirectFactory:

    def to_frontend(self, frontend_url: str) -> RedirectResponse:
        return RedirectResponse(url=frontend_url)
