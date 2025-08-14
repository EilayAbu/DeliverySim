# 🚚 DeliverySim

DeliverySim is a Python-based delivery management system.  
It includes separate menus for Customers, Couriers, and Managers, with support for order tracking, courier assignments (manual and automatic), and distance calculation using Google Maps API or offline mode.

---

## 📌 Features

### Customers
- Register and log in
- Create new delivery orders (pickup from my address or another location)
- View active orders
- View order history

### Couriers
- View orders assigned to you
- Update order status (`picked_up`, `in_transit`, `delivered`)

### Managers
- Register a new courier
- View all active orders
- Manually assign couriers
- Automatically assign the nearest courier
- View analytics:
  - Average delivery time
  - Regional delivery loads
  - List of active couriers

---

## 📂 Project Structure

```
DeliverySim/
│
├── main.py                  # Entry point, menus & role routing
├── DispatchSystem.py        # Core delivery & courier management logic
├── Customer.py              # Customer class
├── Courier.py               # Courier class
├── Manager.py               # Manager class
├── Order.py                 # Order class + unique ID generation functions
│
├── customer_utils.py        # CRUD functions for customers (JSON)
├── courier_utils.py         # CRUD functions for couriers (JSON)
├── order_utils.py           # CRUD functions for orders (JSON)
│
├── google_maps_service.py   # Google Maps distance calculation service + offline mode
│
├── data/
│   ├── customers.json
│   ├── couriers.json
│   ├── orders.json
│   ├── manager.json
│   └── users.json
│
└── tests/
    ├── test_order.py
    ├── test_dispatch_system.py
    ├── test_utils.py
    ├── conftest.py
```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DeliverySim.git
   cd DeliverySim
   ```

2. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate     # On macOS / Linux
   venv\Scripts\activate      # On Windows

   pip install -r requirements.txt
   ```

3. **(Optional) Set Google Maps API key**  
   Edit `google_maps_service.py` and set:
   ```python
   GOOGLE_MAPS_API_KEY = "YOUR_API_KEY"
   ```
   If no key is set, the system will use offline mode.

---

## ▶️ Running the Program

```bash
python main.py
```

- Choose login or register
- Select your role (customer / courier / manager)
- Use your role-specific menu

---

## 🧪 Running Tests

The system uses `pytest` for unit testing:

```bash
pytest -v
```

---

## 📡 Google Maps Integration

- **Online mode**: Uses Google Distance Matrix API for accurate distances and times.
- **Offline mode**: Uses predefined city coordinates and Haversine formula.
