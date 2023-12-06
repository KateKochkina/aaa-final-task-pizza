import time
from functools import wraps
from typing import Dict, List, Union, Type

import click


class Pizza:
    """Class to represent a pizza"""

    def __init__(
        self, name: str, ingredients: List[str], size: str, emoji: str = ""
    ) -> None:
        """Initialize the Pizza object with a name,
        list of ingredients, and an optional emoji"""
        self.name = name
        self.ingredients = ingredients
        self.size = size
        self.emoji = emoji
        self.available_sizes = ["L", "XL"]

    def dict(self) -> Dict[str, List[str]]:
        return {self.name: self.ingredients}

    def __eq__(self, other: object) -> bool:
        """Check if two Pizza objects are equal"""
        return (
            isinstance(other, Pizza)
            and self.name == other.name
            and self.ingredients == other.ingredients
        )


class Margherita(Pizza):
    def __init__(self, size: str = "L"):
        super().__init__(
            self.__class__.__name__,
            ["tomato sauce", "mozzarella", "tomatoes"],
            size,
            "🧀",
        )


class Pepperoni(Pizza):
    def __init__(self, size: str = "L"):
        super().__init__(
            self.__class__.__name__,
            ["tomato sauce", "mozzarella", "pepperoni"],
            size,
            "🍕",
        )


class Hawaiian(Pizza):
    def __init__(self, size: str = "L"):
        super().__init__(
            self.__class__.__name__,
            ["tomato sauce", "mozzarella", "chicken", "pineapples"],
            size,
            "🍍",
        )


def pizza_types() -> List[Type[Pizza]]:
    return [Margherita, Pepperoni, Hawaiian]


def menu():
    for pizza_type in pizza_types():
        pizza = pizza_type()
        click.echo(
            f"{pizza.name}{pizza.emoji} ({pizza.available_sizes}):"
            f' {", ".join(pizza.ingredients)}'
        )


def get_pizza(name: str, size: str) -> Union[Pizza, None]:
    return next(
        (
            pizza_type(size)
            for pizza_type in pizza_types()
            if pizza_type.__name__ == name
        ),
        None,
    )


def order_command(pizza_name: str, size: str, delivery: bool):
    """Prepare and deliver or for pickup the specified pizza"""
    pizza = get_pizza(pizza_name, size)
    if pizza is None:
        print("Такой пиццы нет в меню")
    else:
        bake(pizza)
        if delivery:
            delivery_pizza(pizza)
        else:
            pickup(pizza)


@click.group()
def cli():
    """Main command group"""
    pass


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.argument("pizza", nargs=1, type=str)
def order(pizza: str, delivery: bool):
    size = input("Введите размер пиццы (например, L, XL): ")
    order_command(pizza, size, delivery)


@cli.command()
def show_menu():
    """Show the available menu"""
    menu()


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
def bake(pizza):
    """Bake the pizza"""
    time.sleep(0.5)


@log("🚚 Доставили за {1} с!")
def delivery_pizza(pizza):
    """Deliver the pizza"""
    time.sleep(0.7)


@log("🏠 Забрали за {1} с!")
def pickup(pizza):
    """Pizza pickup"""
    time.sleep(0.3)


if __name__ == "__main__":
    cli()
    