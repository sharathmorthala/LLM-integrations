"""
User Service

Handles basic user operations such as creation
and retrieval. This is a mock service for demo purposes.
"""


class UserService:
    def create_user(self, username: str, email: str):
        return {"id": 1, "username": username, "email": email, "status": "ACTIVE"}

    def get_user(self, user_id: int):
        return {
            "id": user_id,
            "username": "demo_user",
            "email": "demo@example.com",
            "status": "ACTIVE",
        }
