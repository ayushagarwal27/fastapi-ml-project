from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from app.core.config import settings


def create_token(data:dict, expire_minutes:int=30):
    payload = data.copy()
    expire_in = datetime.now(timezone.utc)+ timedelta(minutes=expire_minutes)
    payload.update({'exp':expire_in})
    return jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )


def verify_token(token:str):
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM
        )
        return payload
    except JWTError:
        return None