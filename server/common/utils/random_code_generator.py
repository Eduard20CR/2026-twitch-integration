class RandomCodeGenerator:
    @staticmethod
    def generate_random_code(length=6):
        import random
        import string

        characters = string.ascii_uppercase + string.digits
        return "".join(random.choice(characters) for _ in range(length))
