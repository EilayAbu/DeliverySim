class Manager:
    def __init__(self, name, dispatch_system):
        self.name = name
        self.dispatch_system = dispatch_system

    # This defines a method to see all active (not yet delivered) orders.
    def view_active_orders(self):
        """Return all orders that are not yet delivered."""
        return self.dispatch_system.get_active_orders() #It asks the dispatch system to give it the current active orders.

    # This method allows the manager to manually assign an order to a courier using their IDs.
    def manually_assign_order(self, order_id, courier_id):
        """Assign a specific order to a specific courier."""
        return self.dispatch_system.assign_order_to_courier(order_id, courier_id) #The manager does not do the actual assignment — it asks the dispatch system to do it.

    #This method is for automatic assignment – matching orders to couriers automatically.
    def auto_assign_orders(self):
        """Automatically assign all unassigned orders to matching couriers."""
        return self.dispatch_system.auto_assign_orders() #It asks the dispatch system to do the logic for auto-assigning all unassigned orders.

    #This method gathers data and statistics from the system:Average delivery time, Load (number of orders) by region, Active couriers
    def get_analytics(self):
        """
        Return analytics including:
        - Average delivery time
        - Regional delivery loads
        - List of active couriers
        """
        
        # These three lines each call the dispatch system to get one type of data:Average delivery time in minutes, How many orders are in each region, Which couriers are currently working
        avg_delivery_time = self.dispatch_system.get_average_delivery_time()
        region_loads = self.dispatch_system.get_region_loads()
        active_couriers = self.dispatch_system.get_active_couriers()
        
        # These values are returned as a dictionary (a key-value object), so it's easy to use in reports or GUI.
        return {
            "average_delivery_time": avg_delivery_time,
            "region_loads": region_loads,
            "active_couriers": active_couriers
        }

    def __str__(self):
        return f"Manager: {self.name}"