import uuid

class Customer:
    
    def __init__(self, customer_id, name, address, phone): #Constructor to initialize customer details
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.phone = phone

    def get_details(self): #Method to get customer details
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "address": self.address,
            "phone": self.phone
        }
    
    def get_order_ID(self):
        return self.order_ID

    