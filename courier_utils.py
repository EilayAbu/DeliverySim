import json
import os
from Courier import Courier

FILENAME = "data/couriers.json"

def _load_all_couriers():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Corrupted JSON. Returning empty list.")
            return []

def _save_all_couriers(couriers):
    os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
    with open(FILENAME, "w") as f:
        json.dump(couriers, f, indent=4)

def courier_exists(courier_id):
    couriers = _load_all_couriers()
    return any(c["courier_id"] == courier_id for c in couriers)

def add_courier(courier):
    couriers = _load_all_couriers()
    if courier_exists(courier.courier_id):
        print(f"Courier {courier.courier_id} already exists.")
        return
    couriers.append({
        "name": courier.name,
        "courier_id": courier.courier_id,
        "region": courier.courier_region,
        "deliveries": courier.deliveries
    })
    _save_all_couriers(couriers)
    print(f"Courier {courier.courier_id} added.")

def update_courier(courier):
    couriers = _load_all_couriers()
    for i, c in enumerate(couriers):
        if c["courier_id"] == courier.courier_id:
            couriers[i] = {
                "name": courier.name,
                "courier_id": courier.courier_id,
                "region": courier.courier_region,
                "deliveries": courier.deliveries
            }
            _save_all_couriers(couriers)
            print(f"Courier {courier.courier_id} updated.")
            return
    print("Courier not found for update.")

def delete_courier(courier_id):
    couriers = _load_all_couriers()
    new_couriers = [c for c in couriers if c["courier_id"] != courier_id]
    if len(new_couriers) == len(couriers):
        print("Courier not found.")
        return
    _save_all_couriers(new_couriers)
    print(f"Courier {courier_id} deleted.")

def get_all_couriers():
    return _load_all_couriers()

def get_courier_by_id(courier_id):
    couriers = _load_all_couriers()
    for c in couriers:
        if c["courier_id"] == courier_id:
            return c
    return None
