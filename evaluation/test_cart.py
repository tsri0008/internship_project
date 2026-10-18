"""Medium task evaluator for cart.py, class shopping_cart.

Assumed contract (also put these in BOTH copies of the medium TASK.md):
- add_item(item, price, quantity): nonempty name, nonnegative numeric price,
  positive integer quantity; repeated name with same price accumulates quantity;
  repeated name with different price raises ValueError.
- remove_item(item): removes the entire product, if present; missing is a no-op.
- get_subtotal(): sum of price * quantity, or 0 for an empty cart.
- get_total(subtotal, percentage): apply 0..100 percent discount and round to 2dp.
- list_items(): list of product-name strings.

Set AGENTFLOW_TARGET to the absolute path of the code to evaluate.
"""
import importlib.util
import os
from pathlib import Path

import pytest

DEFAULT_TARGET = Path(__file__).resolve().parent.parent / "tasks" / "medium" / "cart.py"
TARGET = Path(os.environ.get("AGENTFLOW_TARGET", str(DEFAULT_TARGET))).resolve()
spec = importlib.util.spec_from_file_location("agentflow_medium_target", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Cannot load target: {TARGET}")
cart_task = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cart_task)


@pytest.fixture
def cart():
    return cart_task.shopping_cart()


def test_new_cart_is_empty(cart):
    assert cart.get_subtotal() == 0
    assert cart.list_items() == []


def test_add_one_product(cart):
    cart.add_item("Apple", 2, 3)
    assert cart.items["Apple"] == {"price": 2, "quantity": 3}


def test_add_two_different_products(cart):
    cart.add_item("Apple", 2, 3)
    cart.add_item("Milk", 5, 2)
    assert set(cart.list_items()) == {"Apple", "Milk"}
    assert cart.get_subtotal() == pytest.approx(16)


def test_add_existing_product_accumulates_quantity(cart):
    cart.add_item("Apple", 2, 1)
    cart.add_item("Apple", 2, 4)
    assert cart.items["Apple"]["quantity"] == 5
    assert cart.get_subtotal() == pytest.approx(10)


def test_add_existing_product_with_new_price_rejected(cart):
    cart.add_item("Apple", 2, 1)
    with pytest.raises(ValueError):
        cart.add_item("Apple", 4, 1)
    assert cart.items["Apple"] == {"price": 2, "quantity": 1}


@pytest.mark.parametrize("bad_quantity", [0, -1, 1.5, "2"])
def test_invalid_quantities_rejected(cart, bad_quantity):
    with pytest.raises(ValueError):
        cart.add_item("Apple", 2, bad_quantity)


@pytest.mark.parametrize("bad_price", [-1, -0.01])
def test_negative_prices_rejected(cart, bad_price):
    with pytest.raises(ValueError):
        cart.add_item("Apple", bad_price, 1)


def test_zero_price_is_valid(cart):
    cart.add_item("Gift", 0, 2)
    assert cart.get_subtotal() == 0


def test_empty_product_name_rejected(cart):
    with pytest.raises(ValueError):
        cart.add_item("", 2, 1)


def test_remove_existing_product(cart):
    cart.add_item("Apple", 2, 3)
    cart.add_item("Milk", 5, 2)
    cart.remove_item("Apple")
    assert "Apple" not in cart.items
    assert cart.get_subtotal() == pytest.approx(10)


def test_remove_missing_product_does_not_crash(cart):
    cart.remove_item("Not in cart")
    assert cart.list_items() == []


def test_subtotal_uses_quantities_and_prices(cart):
    cart.add_item("Apples", 1.25, 4)
    cart.add_item("Bread", 3.50, 2)
    assert cart.get_subtotal() == pytest.approx(12)


@pytest.mark.parametrize("subtotal,percentage,expected", [
    (100, 0, 100),
    (100, 20, 80),
    (200, 25, 150),
    (100, 100, 0),
    (99.99, 15, 84.99),
])
def test_percentage_discount(subtotal, percentage, expected, cart):
    assert cart.get_total(subtotal, percentage) == pytest.approx(expected)


@pytest.mark.parametrize("invalid_percentage", [-1, 101])
def test_invalid_discount_percentage(cart, invalid_percentage):
    with pytest.raises(ValueError):
        cart.get_total(100, invalid_percentage)


def test_product_names_are_plain_strings(cart):
    cart.add_item("Apple", 2, 1)
    cart.add_item("Milk", 5, 1)
    assert cart.list_items() == ["Apple", "Milk"]
