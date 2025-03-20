from ..api_client import APIClient

class SubscriptionsController:
    """Класс для работы с подписками."""

    def __init__(self):
        self.api = APIClient()

    async def get_subscription_info(self, shortUuid):
        return await self.api.request("GET", f"/sub/{shortUuid}/info")

    async def get_subscription(self, shortUuid):
        return await self.api.request("GET", f"/sub/{shortUuid}")
