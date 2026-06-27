from fastapi import HTTPException, Request


def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")

    if not token:
        raise HTTPException(status_code=401)

    return token
