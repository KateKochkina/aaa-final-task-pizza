import time

import pytest
from pizza import Pizza, PizzaL, PizzaXL, order_command, log


def test_eq_same_pizza():
    pizza1 = Pizza("Margherita", ["tomato sauce",
                   "mozzarella", "tomatoes"], "🧀")
    pizza2 = Pizza("Margherita", ["tomato sauce",
                   "mozzarella", "tomatoes"], "🧀")
    assert pizza1 == pizza2


def test_eq_different_pizza():
    pizza1 = Pizza("Margherita", ["tomato sauce",
                   "mozzarella", "tomatoes"], "🧀")
    pizza2 = Pizza("Pepperoni", ["tomato sauce",
                   "mozzarella", "pepperoni"], "🍕")
    assert not pizza1 == pizza2


def test_eq_different_sizes():
    pizza1 = PizzaL("Margherita", ["tomato sauce",
                    "mozzarella", "tomatoes"], "🧀")
    pizza2 = PizzaXL("Margherita_big", [
                     "tomato sauce", "mozzarella", "tomatoes"], "🧀")
    assert not pizza1 == pizza2


def test_do_nothing_if_pizza_name_not_in_menu(capsys):
    order_command('Not a pizza', delivery=False)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_order_pizza(capsys):
    order_command('Margherita', delivery=True)
    captured = capsys.readouterr()
    assert "👨‍🍳 Приготовили за" in captured.out
    assert "🚚 Доставили за" in captured.out


def test_order_pizza_pickup(capsys):
    order_command('Pepperoni', delivery=False)
    captured = capsys.readouterr()
    assert "👨‍🍳 Приготовили за" in captured.out
    assert "🏠 Забрали за" in captured.out


def test_time_is_measured_correctly_with_log(capsys):
    @log('{1}')
    def calling_function():
        time.sleep(0.1)

    calling_function()
    captured = capsys.readouterr()
    real_time = float(captured.out)
    assert real_time == pytest.approx(0.1, 0.01)
