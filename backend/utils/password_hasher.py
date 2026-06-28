import bcrypt


class PasswordHasher:

    @staticmethod
    def create_hash(
        password: str
    ) -> str:

        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password.decode('utf-8')


    @staticmethod
    def verify_hash(
        password,
        hashed_password
    ) -> bool:

        print("PASSWORD:", password, type(password))
        print("HASH:", hashed_password, type(hashed_password))

        return bcrypt.checkpw(
            str(password).encode("utf-8"),
            str(hashed_password).encode("utf-8")
        )
