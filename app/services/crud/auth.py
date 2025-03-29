from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from database.config import Settings


class auth():
    def __init__(self):
        self.settings = Settings()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def get_auth_data(self) -> dict:
        return {"secret_key": self.settings.SECRET_KEY, "algorithm": self.settings.ALGORITHM}
    
    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        auth_data = self.get_auth_data()
        encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        return encode_jwt
