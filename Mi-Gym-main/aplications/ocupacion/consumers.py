# aplications/ocupacion/consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class OccupancyConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("occupancy", self.channel_name)
        await self.accept()
        # send initial state
        await self.send_json({"count": await self.get_count()})

    async def disconnect(self, code):
        await self.channel_layer.group_discard("occupancy", self.channel_name)

    async def occupancy_message(self, event):
        payload = event.get("payload") or {}
        await self.send_json(payload)

    async def get_count(self):
        # avoid DB in ASGI sync; use sync_to_async in real app
        from .utils import get_current_occupancy
        return get_current_occupancy()
