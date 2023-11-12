
import os #voor github secrets

# pip install python-multipart      (deze stond niet in de cursus)
# pip install "passlib[bcrypt,argon2]"
from passlib.context import CryptContext
import crud

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
#ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
ACCESS_TOKEN_EXPIRE_MINUTES = 30

#HASHING
def get_password_hash(password):
    return pwd_context.hash(password)

#0Auth
pwd_context = CryptContext(schemes=["bcrypt", "argon2"], deprecated="auto")
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_author_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

#token
def create_access_token(data: dict):
    to_encode = data.copy()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 15 minutes of expiration time if ACCESS_TOKEN_EXPIRE_MINUTES variable is empty
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Adding the JWT expiration time case
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

