import hashlib
import random
import string


class RefreshTokenHandler:

    def generate_random_code(self, length=6):
        characters = string.ascii_uppercase + string.digits
        return "".join(random.choice(characters) for _ in range(length))

    def hash_code(self, code):
        return hashlib.sha256(code.encode()).hexdigest()

    def verify_code(self, code, hashed_code):
        return self.hash_code(code) == hashed_code
