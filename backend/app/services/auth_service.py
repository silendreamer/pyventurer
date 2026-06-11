import os
import uuid
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from fastapi import HTTPException

from app.db.connection import get_connection
from app.repositories.user_repository import UserRepository, user_repository

SECRET_KEY = os.environ.get("PYVENTURER_SECRET_KEY", "dev-secret-change-in-production!!")
TOKEN_EXPIRY_DAYS = 7


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def register(self, email: str, name: str, password: str, anonymous_user_id: str | None = None) -> dict:
        if self.users.get_by_email(email):
            raise HTTPException(status_code=409, detail="Email already registered")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        user_id = str(uuid.uuid4())
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = self.users.create_user(user_id, email, name, password_hash)

        if anonymous_user_id:
            self._merge_progress(anonymous_user_id, user_id)

        token = self._create_token(user_id)
        return {"user": user, "token": token}

    def login(self, email: str, password: str) -> dict:
        user = self.users.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = self._create_token(user["id"])
        return {
            "user": {"id": user["id"], "email": user["email"], "name": user["name"]},
            "token": token,
        }

    def get_current_user(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = self.users.get_by_id(payload["sub"])
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        return {"id": user["id"], "email": user["email"], "name": user["name"]}

    def _create_token(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.now(timezone.utc) + timedelta(days=TOKEN_EXPIRY_DAYS),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def _merge_progress(self, anonymous_user_id: str, user_id: str) -> None:
        conn = get_connection()
        conn.execute(
            "UPDATE learner_profiles SET user_id = ? WHERE anonymous_user_id = ?",
            (user_id, anonymous_user_id),
        )
        conn.execute(
            "UPDATE progress SET user_id = ? WHERE anonymous_user_id = ?",
            (user_id, anonymous_user_id),
        )
        conn.commit()


auth_service = AuthService(user_repository)
