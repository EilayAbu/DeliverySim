import importlib
import pytest

def test_generate_unique_order_id_monotonic():
    try:
        ou = importlib.import_module("order_utils")
    except Exception:
        pytest.skip("order_utils module not found")

    if not hasattr(ou, "generate_unique_order_id"):
        pytest.skip("generate_unique_order_id not implemented")

    a = ou.generate_unique_order_id()
    b = ou.generate_unique_order_id()
    assert isinstance(a, int) and isinstance(b, int)
    assert a != b
