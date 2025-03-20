from ..api_client import APIClient

class NodesController:
    """Класс для управления серверами (нодами)."""

    def __init__(self):
        self.api = APIClient()

    async def create_node(self, **data):
        return await self.api.request("POST", "/nodes/create", json=data)

    async def get_all_nodes(self):
        return await self.api.request("GET", "/nodes/get-all")

    async def get_one_node(self, uuid):
        return await self.api.request("GET", f"/nodes/get-one/{uuid}")

    async def enable_node(self, uuid):
        return await self.api.request("PATCH", f"/nodes/enable/{uuid}")

    async def disable_node(self, uuid):
        return await self.api.request("PATCH", f"/nodes/disable/{uuid}")

    async def delete_node(self, uuid):
        return await self.api.request("DELETE", f"/nodes/delete/{uuid}")

    async def restart_node(self, uuid):
        return await self.api.request("GET", f"/nodes/restart/{uuid}")

    async def restart_all_nodes(self):
        return await self.api.request("PATCH", "/nodes/restart-all")
