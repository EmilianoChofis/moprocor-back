from datetime import timedelta, datetime

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt, JWTError
from starlette import status

from models.auth import TokenData
from models.user import User
from repositories.user_repository import UserRepository

SECRET_KEY = "secret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    """
    Authentication service for user management.
    """

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    async def autenticate_user(username: str, password: str):
        user = await UserRepository.get_user_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado",
            )
        if not AuthService.verify_password(password, user.hashed_password):
            return False
        return user

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(token: str = Depends(oauth_2_scheme)):
        credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                              detail="No podemos validar las credenciales",
                                              headers={"WWW-Authenticate": "Bearer"})

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception

            token_data = TokenData(username=username)

        except JWTError:
            raise credentials_exception

        user = await UserRepository.get_user_by_username(token_data.username)
        if user is None:
            raise credentials_exception

        return user

    @staticmethod
    async def get_current_active_user(current_user: User = Depends(get_current_user)):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Usuario inactivo")
        return current_user