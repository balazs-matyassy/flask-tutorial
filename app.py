import functools
import math

from flask import Flask, render_template


def buy_1_get_2(func):
    @functools.wraps(func)
    def wrapped_view(quantity):
        new_quantity = math.ceil(quantity / 2)

        return func(new_quantity)

    return wrapped_view


def tax(func):
    @functools.wraps(func)
    def wrapped_view(*args, **kwargs):
        net = func(*args, **kwargs)
        gross = round(net * 1.25)

        return gross

    return wrapped_view


app = Flask(__name__)


@app.route('/')
def home():
    return render_template(
        'home.html',
        android_price=get_android_price(10),
        energy_price=get_energy_price(10),
        spaceship_price=get_spaceship_price(10)
    )


@buy_1_get_2
@tax
def get_android_price(quantity=1):
    return quantity * 25_000


@tax
def get_energy_price(quantity=1):
    return quantity * 10


@tax
def get_spaceship_price(quantity=1):
    return quantity * 750_000


if __name__ == '__main__':
    app.run()
