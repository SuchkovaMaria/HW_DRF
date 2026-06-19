import os

import stripe

stripe.api_key = os.getenv("STRIPE_API_KEY")

def create_stripe_product(course):
  """Создание продукта - курса"""

  return stripe.Product.create(name=course)


def create_stripe_price(course,amount):
  """Создание цены курса"""

  product = create_stripe_product(course)
  return stripe.Price.create(
    currency="rub",
    unit_amount= int(amount*100),
    product= product.id
  )

def create_stripe_sessions(price):
  """Создание сессии"""

  session = stripe.checkout.Session.create(
    success_url="http://127.0.0.1:8000/success",
    line_items=[{"price": price.id, "quantity": 1}],
    mode="payment",
  )
  return session.id, session.url