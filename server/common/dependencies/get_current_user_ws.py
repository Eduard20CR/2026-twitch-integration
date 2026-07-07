import token

from fastapi import Depends, Request, HTTPException, WebSocket

from common.tokens.jwt_token_handler import JWTTokenHandler
from common.dates.date_delay_generator import DateDelayGenerator


def get_jwt_handler_ws(request: WebSocket) -> JWTTokenHandler:
    return request.app.state.jwt_handler


def get_date_delay_generator_ws(request: WebSocket) -> DateDelayGenerator:
    return request.app.state.date_delay_generator


def get_current_user_ws(
    websocket: WebSocket,
    jwt: JWTTokenHandler = Depends(get_jwt_handler_ws),
    date_delay_generator: DateDelayGenerator = Depends(get_date_delay_generator_ws),
):
    token = websocket.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401)

    payload = jwt.decode_token(token)

    if not payload:
        raise HTTPException(status_code=401)

    if payload.get("exp") < date_delay_generator.get_current_utc_time().timestamp():
        raise HTTPException(status_code=401)

    return payload
