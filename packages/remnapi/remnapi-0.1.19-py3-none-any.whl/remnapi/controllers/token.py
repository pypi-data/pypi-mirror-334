from ..api_client import APIClient

class TokenController:

    def __init__(self):
        self.api = APIClient()
    
    async def create_token(self, **kwargs):
        data = {**kwargs}
        return await self.api.request("POST", "/tokens/create", json=data)  # Используем JWT токен
