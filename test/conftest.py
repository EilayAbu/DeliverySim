import json
import pytest
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]  
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
@pytest.fixture
def sample_orders():
    """Example orders used across tests."""
    return [
        {
            "order_id": 10000, 
            "customer_id": 1003,
            "pickup_location": "Haifa", 
            "destination": "Beer Sheva",
            "status": "delivered", 
            "date": "2025-08-07T15:28:00", 
            "courier_id": 2003
        },
        {
            "order_id": 10002, 
            "customer_id": 1002,
            "pickup_location": "Tel Aviv", 
            "destination": "Holon",
            "status": "in_transit", 
            "date": "2025-08-07T15:28:00", 
            "courier_id": 2001
        },
        {
            "order_id": 10007, 
            "customer_id": 1001,
            "pickup_location": "Jerusalem", 
            "destination": "Petah Tikva",
            "status": "pending", 
            "date": "2025-08-07T15:28:00", 
            "courier_id": None
        },
    ]

@pytest.fixture
def sample_couriers():
    return [
        {"courier_id": 2001, "name": "Dana",
         "current_location": "Rothschild Blvd 1, Tel Aviv-Yafo, Israel",
         "location": "Rothschild Blvd 1, Tel Aviv-Yafo, Israel",   
         "region": "center",                                       
         "available": True},
        {"courier_id": 2002, "name": "Eli",
         "current_location": "HaNassi Blvd 109, Haifa, Israel",
         "location": "HaNassi Blvd 109, Haifa, Israel",            
         "region": "north",                                        
         "available": True},
        {"courier_id": 2003, "name": "Noa",
         "current_location": "Jerusalem, Israel",
         "location": "Jerusalem, Israel",                          
         "region": "jerusalem",                                    
         "available": False},
    ]


@pytest.fixture
def tmp_orders_file(tmp_path, sample_orders):
    p = tmp_path / "orders.json"
    p.write_text(json.dumps(sample_orders, indent=2), encoding="utf-8")
    return str(p)

@pytest.fixture
def tmp_couriers_file(tmp_path, sample_couriers):
    p = tmp_path / "couriers.json"
    p.write_text(json.dumps(sample_couriers, indent=2), encoding="utf-8")
    return str(p)

@pytest.fixture
def fake_maps(mocker):
    """Replaces the real Google Maps call with a deterministic response.
    Adjust the dotted path below to match your project if needed.
    """
    try:
        mocker.patch(
            "google_maps_service.get_distance_and_duration",
            return_value={"distance_km": 5.0, "duration_min": 12.0}
        )
    except Exception:
        pass

    class FakeMaps:
        def get_distance_and_duration(self, origin_address: str, dest_address: str, allow_fallback: bool = True):
            return {"distance_km": 5.0, "duration_min": 12.0}

    return FakeMaps()
