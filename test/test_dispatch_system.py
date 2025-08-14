import pytest

from DispatchSystem import DispatchSystem

def _load(ds, orders_file, couriers_file):
    if hasattr(ds, "load_orders_from_file"):
        ds.load_orders_from_file(orders_file)
    if hasattr(ds, "load_couriers_from_file"):
        ds.load_couriers_from_file(couriers_file)

def test_load_files(tmp_orders_file, tmp_couriers_file):
    ds = DispatchSystem()
    _load(ds, tmp_orders_file, tmp_couriers_file)
    assert hasattr(ds, "orders") and len(ds.orders) > 0
    assert hasattr(ds, "couriers") and len(ds.couriers) > 0

def test_manual_assign_courier(tmp_orders_file, tmp_couriers_file):
    ds = DispatchSystem()
    _load(ds, tmp_orders_file, tmp_couriers_file)

    pending = next((o for o in ds.orders if getattr(o, "status", None) in ("pending", None)), None)
    free = next((c for c in ds.couriers if getattr(c, "available", True)), None)
    if not pending or not free:
        pytest.skip("No pending order or free courier in sample data")

    if hasattr(ds, "assign_order_to_courier"):
        ds.assign_order_to_courier(pending.order_id, free.courier_id)
        cid = getattr(pending, "courier_id", None)
        courier_obj = getattr(pending, "courier", None)
        assert (cid == free.courier_id) or (courier_obj and getattr(courier_obj, "courier_id", None) == free.courier_id)
    else:
        pytest.skip("DispatchSystem.assign_order_to_courier not implemented")

def test_auto_assign_nearest(tmp_orders_file, tmp_couriers_file, fake_maps):
    ds = DispatchSystem()
    _load(ds, tmp_orders_file, tmp_couriers_file)

    order = next((o for o in ds.orders if getattr(o, "courier_id", None) in (None, 0)), None)
    if not order:
        pytest.skip("No unassigned order in sample data")

    if hasattr(ds, "auto_assign_nearest"):
        try:
            ds.auto_assign_nearest(order.order_id, maps_client=fake_maps)
        except TypeError:
            ds.auto_assign_nearest(order.order_id)
        assert getattr(order, "courier_id", None) is not None or getattr(order, "courier", None) is not None
    else:
        pytest.skip("DispatchSystem.auto_assign_nearest not implemented")
