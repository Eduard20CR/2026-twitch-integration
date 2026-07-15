from cryptography.fernet import Fernet


class EncryptionService:
    def __init__(self, key: str):
        self.cipher = Fernet(key.encode())

    def encrypt(self, value: str) -> str:
        return self.cipher.encrypt(value.encode()).decode()

    def decrypt(self, encrypted_value: str) -> str:
        return self.cipher.decrypt(encrypted_value.encode()).decode()
