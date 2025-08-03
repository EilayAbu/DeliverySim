# import uuid

# class Customer:
    
#     def __init__(self, customer_id, name, address, phone): #Constructor to initialize customer details
#         self.customer_id = customer_id
#         self.name = name
#         self.address = address
#         self.phone = phone

#     def get_details(self): #Method to get customer details
#         return {
#             "customer_id": self.customer_id,
#             "name": self.name,
#             "address": self.address,
#             "phone": self.phone
#         }
    
#     def get_order_ID(self):
#         return self.order_ID

   
import uuid

class Customer:
    def __init__(self,customer_id ,name, address, phone):
        if not customer_id:
            customer_id = str(uuid.uuid4())[:8]
        else:
            self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone
        self.order_history = []  # ← השורה החסרה!

    def get_details(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone
        }

    def __str__(self):
        return f"{self.name} ({self.customer_id})"

    def create_order(self, destination, item_description, weight=1.0):
        from Order import Order
        order = Order(str(uuid.uuid4())[:8], self.customer_id, destination)
        order.item_description = item_description
        order.weight = weight
        self.order_history.append(order.order_id)
        return order
    
    def get_active_orders(self, all_orders):
        return [
            order for order in all_orders
            if str(order.customer_id) == str(self.customer_id)
            and order.status not in ['delivered', 'cancelled']
        ]


