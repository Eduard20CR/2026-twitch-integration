from fastapi import Depends, Request, HTTPException


def get_jwt_handler(request: Request):
    return request.app.state.jwt_handler


def get_current_user(request: Request, jwt=Depends(get_jwt_handler)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401)

    payload = jwt.decode_token(token)

    if not payload:
        raise HTTPException(status_code=401)

    return payload
