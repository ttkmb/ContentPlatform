import os

import stripe

stripe.api_key = os.getenv('STRIPE_API_KEY')


def create_stripe_items(name):
    product_names = [stripe.Product.create(name=product)['name'] for product in name]
    return product_names


def create_stripe_price(price, products_name):
    product_ids = stripe.Price.create(currency="rub",
                                      unit_amount=price * 100,
                                      product_data={"name": products_name})
    return product_ids["id"]


def create_stripe_session(stripe_price_id):
    stripe_session = stripe.checkout.Session.create(
        success_url="http://localhost:8000",
        line_items=[
            {
                "price": stripe_price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
    )
    return stripe_session["url"], stripe_session["id"]


def check_stripe_completed(session_id):
    stripe_session = stripe.checkout.Session.retrieve(session_id).status
    if stripe_session == 'complete':
        return True
    return False
