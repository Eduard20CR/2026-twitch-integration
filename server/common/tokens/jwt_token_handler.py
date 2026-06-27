import jwt
from typing import Any, Dict, List, Optional


class JWTTokenHandler:
    def __init__(self, jwt_secret_key: str, algorithm: str = "HS256"):
        self.jwt_secret_key = jwt_secret_key
        self.algorithm = algorithm

    def generate_token(self, payload: Dict[str, Any]) -> str:
        """
        Generate a JWT token.
        """
        return jwt.encode(payload, self.jwt_secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str, algorithms: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Decode and validate a JWT token.
        Raises jwt exceptions if invalid.
        """
        if algorithms is None:
            algorithms = [self.algorithm]

        return jwt.decode(token, self.jwt_secret_key, algorithms=algorithms)
