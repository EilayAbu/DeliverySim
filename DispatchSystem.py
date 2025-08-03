from collections import defaultdict
from datetime import datetime
import Courier as courier
import Order as order
import heapq
import json
import os
import googlemaps


class DispatchSystem:
    def __init__(self):
        self.orders = []
        self.couriers = []
        self.gmaps = googlemaps.Client(key="AIzaSyDeR71F-MwYPNnJZUNP1I-xyfCjybdw4MA")  # ← החליפי ב־API שלך
        self.load_couriers_from_file()
        self.load_orders_from_file()

    def assign_to_closest_courier_by_distance(self, order):
        destination_address = order.destination.strip()

        closest_courier = None
        shortest_time = float("inf")

        try:
        # נוודא שהכתובת בכלל תקפה לפני הכל
            geocode_result = self.gmaps.geocode(destination_address)
            if not geocode_result:
                print("❌ Invalid destination address.")
                return False  # ביטול יצירת הזמנה
        except Exception:
            print("❌ Failed to verify destination address.")
            return False

        for c in self.couriers:
            try:
                result = self.gmaps.distance_matrix(
                    origins=[c.courier_region],
                    destinations=[destination_address],
                    mode="driving"
                )
                element = result["rows"][0]["elements"][0]
                if element["status"] != "OK":
                    continue

                duration = element["duration"]["value"]  # שניות

                if duration < shortest_time:
                    shortest_time = duration
                    closest_courier = c

            except Exception:
                continue  # לא להדפיס הודעה – נשאר שקט

        if closest_courier:
            order.courier = closest_courier
            order.status = "assigned"
            closest_courier.assign_order(order.order_id)
            self.save_orders_to_file()
            print(f"✅ Order {order.order_id} assigned to closest courier: {closest_courier.name}")
            return True
        else:
            print("❌ No available courier found for this location.")
            return False


    def assign_order_to_courier(self, order_id, courier_id):
        for o in self.orders:
            if o.order_id == order_id:
                courier_obj = courier.find_courier_by_id(courier_id)
                if courier_obj and not o.is_assigned():
                    o.assign_to(courier_obj)
                    print(f"Order {order_id} assigned to courier {courier_obj.name}.")

    def get_average_delivery_time(self):
        total_time = 0
        delivered_orders = 0
        for o in self.orders:
            if o.status == "delivered" and hasattr(o, 'date'):
                try:
                    if isinstance(o.date, str):
                        date_obj = datetime.strptime(o.date, "%Y-%m-%d %H:%M:%S")
                    else:
                        date_obj = o.date
                    elapsed = (datetime.now() - date_obj).total_seconds() / 3600
                    total_time += elapsed
                    delivered_orders += 1
                except Exception:
                    continue
        return total_time / delivered_orders if delivered_orders > 0 else 0

    def load_couriers_from_file(self, filename="couriers.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f:
            data = json.load(f)
            for entry in data:
                c = courier.Courier(entry["name"], entry["courier_id"], entry["region"])
                c.deliveries = entry.get("deliveries", [])
                self.couriers.append(c)

    def build_courier_load_heap(orders):
        courier_order_counts = defaultdict(int)
        for order in orders:
            if order.courier:
                courier_id = order.courier.courier_id
                courier_order_counts[courier_id] += 1
        courier_heap = [(num_orders, courier_id) for courier_id, num_orders in courier_order_counts.items()]
        heapq.heapify(courier_heap)
        return courier_heap

    def load_orders_from_file(self, filename="orders.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f:
            data = json.load(f)
            for entry in data:
                o = order.Order.from_dict(entry)
                if o.courier_id:
                    o.courier = self.find_courier_by_id(o.courier_id)
                self.orders.append(o)


    def history_of_orders_by_customer(self, customer_id):
        return [o for o in self.orders if o.customer_id == customer_id]

    def add_order(self, order_id, customer_name, delivery_address):
        new_order = order.Order(order_id, customer_name, delivery_address)
        self.orders.append(new_order)
        print(f"Order {order_id} added for {customer_name} at {delivery_address}.")

    def add_order_by_customer(self, order_obj, customer_name, delivery_address):
        if not any(o.order_id == order_obj.order_id for o in self.orders):
            self.orders.append(order_obj)
            print(f"Order {order_obj.order_id} added for {customer_name} at {delivery_address}.")
        else:
            print(f"Order {order_obj.order_id} already exists. Please use a different order ID.")

    def auto_assign_orders(self):
        assigned_any = False
        for o in self.orders:
            if not o.is_assigned():
                matching_couriers = [c for c in self.couriers if c.courier_region.lower() == o.destination.lower()]
                if matching_couriers:
                    best_courier = min(matching_couriers, key=lambda c: len(c.deliveries))
                    o.courier = best_courier
                    o.courier_id = best_courier.courier_id
                    o.status = "assigned"
                    best_courier.assign_order(o.order_id)
                    print(f"✅ Order {o.order_id} assigned to courier {best_courier.name} in region {best_courier.courier_region}.")
                    assigned_any = True
                else:
                    o.status = "unassigned"
                    print(f"⚠️ No couriers available in region '{o.destination}'. Order marked as 'unassigned'.")
        if assigned_any:
            self.save_orders_to_file()


    def assign_order_to_courier(self, order_id, courier_id):
        courier_obj = self.find_courier_by_id(courier_id)
        for o in self.orders:
            if o.order_id == order_id and courier_obj:
                o.courier = courier_obj
                courier_obj.assign_order(order_id)
                print(f"Order {order_id} assigned to courier {courier_obj.name}.")
                return
        print(f"Order or courier not found.")

    def get_active_orders(self):
        return [o for o in self.orders if o.status not in ('delivered', 'cancelled')]

    def update_order_status(self, order_id, new_status):
        for o in self.orders:
            if o.order_id == order_id:
                o.update_status(new_status)
                print(f"Order {order_id} status updated to {new_status}")
                return
        print(f"Order {order_id} not found.")

    def get_orders_for_courier(self, courier_id):
        return [o for o in self.orders if o.courier and o.courier.courier_id == courier_id]

    def save_order_to_file(self, order, filename="orders.json"):
        data = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
        data.append(order.to_dict())
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def save_orders_to_file(self, filename="orders.json"):
        data = [o.to_dict() for o in self.orders]
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def add_courier(self, courier):
        self.couriers.append(courier)
        print(f"Courier {courier.name} (ID: {courier.courier_id}) added.")
        self.save_couriers_to_file()
        self.auto_assign_unassigned_orders(courier)

    def auto_assign_unassigned_orders(self, new_courier):
        assigned_any = False
        for o in self.orders:
            if o.status == "unassigned" and o.destination.lower() == new_courier.courier_region.lower():
                o.courier = new_courier
                o.status = "assigned"
                new_courier.assign_order(o.order_id)
                print(f"✅ Order {o.order_id} assigned to new courier {new_courier.name}.")
                assigned_any = True
        if assigned_any:
            self.save_orders_to_file()

    def courier_update_status(self, courier_id, order_id, status):
        courier = self.find_courier_by_id(courier_id)
        if courier:
            order = self.find_order_by_id(order_id)
            if order and order.courier == courier:
                order.update_status(status)
                print(f"Order {order_id} status updated to {status} by courier {courier.name}.")
                self.save_orders_to_file()
            else:
                print(f"Order {order_id} not found or not assigned to courier {courier.name}.")
        else:
            print(f"Courier {courier_id} not found.")

    def find_courier_by_id(self, courier_id):
        for c in self.couriers:
            if c.courier_id == courier_id:
                return c
        return None

    def save_couriers_to_file(self, filename="couriers.json"):
        data = []
        for c in self.couriers:
            data.append({
                "name": c.name,
                "courier_id": c.courier_id,
                "region": c.courier_region,
                "deliveries": c.deliveries
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def find_available_courier(self):
        return min(self.couriers, key=lambda c: len(c.deliveries), default=None)

    def get_active_couriers(self):
        return [c for c in self.couriers if c.deliveries]

    def get_all_couriers(self):
        return self.couriers

    def get_region_loads(self):
        region_counts = defaultdict(int)
        for o in self.orders:
            if o.courier:
                region_counts[o.courier.courier_region] += 1
        return dict(region_counts)

    def assign_to_nearest_courier(self, order):
        matching_couriers = [c for c in self.couriers if c.courier_region.lower() == order.destination.lower()]
        if matching_couriers:
            best_courier = min(matching_couriers, key=lambda c: len(c.deliveries))
            order.courier = best_courier
            order.courier_id = best_courier.courier_id
            order.status = "assigned"
            best_courier.assign_order(order.order_id)
            print(f"✅ Order {order.order_id} automatically assigned to courier {best_courier.name} in region {best_courier.courier_region}.")
        else:
            order.status = "unassigned"
            print(f"⚠️ No couriers available in region '{order.destination}'. Order marked as 'unassigned'.")

    def get_region_loads(self):
        region_counts = defaultdict(int)
        for o in self.orders:
            if o.courier:
                region_counts[o.courier.courier_region] += 1
        return dict(region_counts)

    def get_delivered_count_by_courier(self):
        delivered_counts = defaultdict(int)
        for o in self.orders:
            if o.status == "delivered" and o.courier_id:
                delivered_counts[o.courier_id] += 1
        return dict(delivered_counts)


def assign_to_closest_courier_by_distance(self, order):
    if not order.pickup_address:
        print("❌ Order missing pickup address.")
        return

    best_courier = None
    shortest_distance = float("inf")

    for courier in self.couriers:
        try:
            origin = courier.courier_region  # use region as location
            destination = order.pickup_address

            result = gmaps.distance_matrix(origin, destination, mode="driving")
            distance_text = result['rows'][0]['elements'][0]['distance']['text']
            distance_value = result['rows'][0]['elements'][0]['distance']['value']  # in meters

            if distance_value < shortest_distance:
                shortest_distance = distance_value
                best_courier = courier
        except Exception as e:
            print(f"Error checking distance for courier {courier.name}: {e}")

    if best_courier:
        order.courier = best_courier
        order.courier_id = best_courier.courier_id
        order.status = "assigned"
        best_courier.assign_order(order.order_id)
        print(f"✅ Order {order.order_id} assigned to {best_courier.name} ({shortest_distance/1000:.2f} km away).")
        self.save_orders_to_file()
    else:
        order.status = "unassigned"
        print("⚠️ No couriers found for assignment.")
