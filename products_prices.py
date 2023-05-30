# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import json
import stripe
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def open_json():
    f = open("./src/subscriptions.json")
    data = json.load(f)
    f.close()
    return data


def main():
    subscriptions = open_json()
    for subscription in subscriptions:
        print(subscription)
        product = stripe.Product.create(
            name=subscription["name"], description=subscription["description"]
        )
        product_id = product["id"]
        if subscription["pricing_model"] == "standard":
            unlimited_price_id = stripe.Price.create(
                product=product_id,
                unit_amount=subscription["unit_amount"],  # $24.99
                currency=subscription["currency"],
                recurring=subscription["recurring"],
                lookup_key=subscription["lookup_key"],
            )
            print(unlimited_price_id)
        elif subscription["pricing_model"] == "graduated":
            metered_price_id = stripe.Price.create(
                tiers=subscription["tiers"],
                currency=subscription["currency"],
                recurring=subscription["recurring"],
                product=product_id,
                tiers_mode="graduated",
                billing_scheme=subscription["billing_scheme"],
                expand=["tiers"],
                lookup_key=subscription["lookup_key"],
            )
            print(metered_price_id)
        print("done")


if __name__ == "__main__":
    main()
