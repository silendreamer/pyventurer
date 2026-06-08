from app.db.connection import get_connection


class UserRepository:
    def create_user(self, user_id: str, email: str, name: str, password_hash: str) -> dict:
        conn = get_connection()
        conn.execute(
            "INSERT INTO users (id, email, name, password_hash) VALUES (?, ?, ?, ?)",
            (user_id, email, name, password_hash),
        )
        conn.commit()
        return {"id": user_id, "email": email, "name": name}

    def get_by_email(self, email: str) -> dict | None:
        conn = get_connection()
        row = conn.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
        if row is None:
            return None
        return dict(row)

    def get_by_id(self, user_id: str) -> dict | None:
        conn = get_connection()
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if row is None:
            return None
        return dict(row)


user_repository = UserRepository()
