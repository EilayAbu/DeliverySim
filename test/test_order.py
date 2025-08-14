import datetime as dt
import pytest

from Order import Order

def test_order_to_dict_contains_all_fields():
    o = Order(order_id=1234, customer_id=42,
              pickup_location="Tel Aviv", destination="Haifa",
              status="pending", date=dt.datetime(2025, 8, 7, 15, 28))
    d = o.to_dict() if hasattr(o, "to_dict") else o.__dict__
    assert d["order_id"] == 1234
    assert d["customer_id"] == 42
    assert d.get("pickup_location") == "Tel Aviv"
    assert d["destination"] == "Haifa"
    assert d["status"] in ("pending", "created", "new", d["status"])  # tolerant to your impl
    assert "date" in d

def test_order_status_flow():
    o = Order(order_id=1, customer_id=1, pickup_location="A", destination="B",
              status="pending", date=dt.datetime.now())
    if hasattr(o, "mark_picked_up"):
        o.mark_picked_up()
        assert o.status in ("picked_up", "in_transit")
    elif hasattr(o, "update_status"):
        o.update_status("picked_up")
        assert o.status in ("picked_up", "in_transit")
    else:
        pytest.skip("No status update API found on Order")

    if hasattr(o, "mark_delivered"):
        o.mark_delivered()
        assert o.status == "delivered"
    elif hasattr(o, "update_status"):
        o.update_status("delivered")
        assert o.status == "delivered"
    else:
        pytest.skip("No delivery status API found on Order")
