from ..api_client import APIClient

class UsersController:
    """Класс для работы с пользователями через API."""

    def __init__(self):
        self.api = APIClient()

    async def create_user(self, username, status="ACTIVE", **kwargs):
        data = {"username": username, "status": status, **kwargs}
        return await self.api.request("POST", "/users", json=data)

    async def update_user(self, user_id, **kwargs):
        return await self.api.request("POST", "/users/update", json={"user_id": user_id, **kwargs})

    async def get_users(self, params=None):
        return await self.api.request("GET", "/users/v2", params=params)

    async def get_user_by_uuid(self, uuid):
        return await self.api.request("GET", f"/users/uuid/{uuid}")

    async def get_user_by_username(self, username):
        return await self.api.request("GET", f"/users/username/{username}")

    async def delete_user(self, user_uuid):
        return await self.api.request("DELETE", f"/users/delete/{user_uuid}")

    async def enable_user(self, uuid):
        return await self.api.request("PATCH", f"/users/enable/{uuid}")

    async def disable_user(self, uuid):
        return await self.api.request("PATCH", f"/users/disable/{uuid}")

    async def reset_user_traffic(self, uuid):
        return await self.api.request("PATCH", f"/users/reset-traffic/{uuid}")
