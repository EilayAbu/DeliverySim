import json
import os
from Customer import Customer

FILENAME = "data/customers.json"

def _load_all_customers():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            print("Warning: Corrupted JSON. Returning empty list.")
            return []

def _save_all_customers(customers):
    os.makedirs(os.path.dirname(FILENAME), exist_ok=True)
    with open(FILENAME, "w") as f:
        json.dump(customers, f, indent=4)

def customer_exists(customer_id):
    customers = _load_all_customers()
    return any(c["customer_id"] == customer_id for c in customers)

def add_customer(customer):
    customers = _load_all_customers()
    if customer_exists(customer.customer_id):
        print(f"Customer {customer.customer_id} already exists.")
        return
    customers.append({
        "customer_id": customer.customer_id,
        "name": customer.name,
        "password": customer.password,
        "address": customer.address,
        "phone": customer.phone
    })
    _save_all_customers(customers)
    print(f"Customer {customer.customer_id} added.")

def update_customer(customer):
    customers = _load_all_customers()
    for i, c in enumerate(customers):
        if c["customer_id"] == customer.customer_id:
            customers[i] = {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "password": customer.password,
                "address": customer.address,
                "phone": customer.phone
            }
            _save_all_customers(customers)
            print(f"Customer {customer.customer_id} updated.")
            return
    print("Customer not found for update.")

def delete_customer(customer_id):
    customers = _load_all_customers()
    new_customers = [c for c in customers if c["customer_id"] != customer_id]
    if len(new_customers) == len(customers):
        print("Customer not found.")
        return
    _save_all_customers(new_customers)
    print(f"Customer {customer_id} deleted.")

def get_all_customers():
    return _load_all_customers()

def get_customer_by_id(customer_id):
    customers = _load_all_customers()
    for c in customers:
        if c["customer_id"] == customer_id:
            return c
    return None