# aplications/ocupacion/utils.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ActiveSession

def get_current_occupancy():
    return ActiveSession.objects.filter(status="ACTIVE").count()

def publish_occupancy_update():
    print(f"[DEBUG] Ocupación actual: {get_current_occupancy()} socios")
