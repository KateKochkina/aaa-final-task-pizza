import time
from functools import wraps
from typing import Dict, List, Union

import click


class Pizza:
    """Class to represent a pizza"""

    def __init__(self, name: str, ingredients: List[str],
                 emoji: str | None = None):
        """Initialize the Pizza object with a name,
        list of ingredients, and an optional emoji"""
        self.name = name
        self.ingredients = ingredients
        self.emoji = emoji if emoji is not None else ""

    def dict(self) -> Dict[str, List[str]]:
        return {self.name: self.ingredients}

    def __eq__(self, other: object) -> bool:
        """Check if two Pizza objects are equal"""
        return (
            isinstance(other, Pizza)
            and self.name == other.name
            and self.ingredients == other.ingredients
        )


class PizzaL(Pizza):
    """Class to represent a large pizza"""

    def __init__(self, name: str, ingredients: List[str],
                 emoji: str | None = None):
        """Initialize the PizzaL object"""
        super().__init__(name, ingredients, emoji)
        self.size = "L"


class PizzaXL(Pizza):
    """Class to represent a big pizza"""

    def __init__(self, name: str, ingredients: List[str],
                 emoji: str | None = None):
        """Initialize the PizzaXL object"""
        super().__init__(name, ingredients, emoji)
        self.size = "XL"


menu: List[Union[PizzaL, PizzaXL]] = [
    PizzaL("Margherita", ["tomato sauce", "mozzarella", "tomatoes"], "🧀"),
    PizzaL("Pepperoni", ["tomato sauce", "mozzarella", "pepperoni"], "🍕"),
    PizzaL("Hawaiian", ["tomato sauce", "mozzarella", "chicken", "pineapples"],
           "🍍"),
    PizzaXL("Margherita_big", ["tomato sauce", "mozzarella", "tomatoes"], "🧀"),
    PizzaXL("Pepperoni_big", ["tomato sauce", "mozzarella", "pepperoni"], "🍕"),
    PizzaXL("Hawaiian_big", ["tomato sauce", "mozzarella", "chicken",
                             "pineapples"], "🍍"),
]


def order_command(pizza: str, delivery: bool):
    """Prepare and deliver or for pickup the specified pizza"""
    for item in menu:
        if item.name.lower() == pizza.lower():
            bake(item)
            if delivery:
                delivery_pizza(item)
            else:
                pickup(item)


def show_menu_command():
    """Display the menu of available pizzas"""
    for pizza in menu:
        click.echo(
            f"{pizza.name}{pizza.emoji} ({pizza.size}):"
            f' {", ".join(pizza.ingredients)}'
        )


@click.group()
def cli():
    """Main command group"""
    pass


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.argument("pizza", nargs=1, type=str)
def order(pizza: str, delivery: bool):
    order_command(pizza, delivery)


@cli.command()
def show_menu():
    """Show the available menu"""
    show_menu_command()


def log(template: str = "{} - {} с"):
    """Decorator to log the execution time of a function"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = round(end_time - start_time, 2)
            click.echo(template.format(func.__name__, execution_time))
            return result

        return wrapper

    return decorator


@log("👨‍🍳 Приготовили за {1} c")
def bake(pizza: Union[PizzaL, PizzaXL]):
    """Bake the pizza"""
    time.sleep(0.5)


@log("🚚 Доставили за {1} с!")
def delivery_pizza(pizza: Union[PizzaL, PizzaXL]):
    """Deliver the pizza"""
    time.sleep(0.7)


@log("🏠 Забрали за {1} с!")
def pickup(pizza: Union[PizzaL, PizzaXL]):
    """Pizza pickup"""
    time.sleep(0.3)


if __name__ == "__main__":
    cli()
