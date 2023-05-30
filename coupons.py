# Set your secret key. Remember to switch to your live secret key in production.
# See your keys here: https://dashboard.stripe.com/apikeys
import json
import stripe
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def open_json():
    f = open("./src/coupons.json")
    data = json.load(f)
    f.close()
    return data


def main():
    coupons = open_json()
    for coupon in coupons:
        print(coupon)
        if "percent_off" in coupon:
            coupon = stripe.Coupon.create(
                duration=coupon["duration"],
                id=coupon["id"],
                percent_off=coupon["percent_off"],
            )
            print(coupon)
            print("Done")
        elif "amount_off" in coupon:
            coupon = stripe.Coupon.create(
                duration=coupon["duration"],
                id=coupon["id"],
                amount_off=coupon["amount_off"],
                currency=coupon["currency"],
                duration_in_months=coupon["duration_in_months"],
            )
            print(coupon)
            print("Done")


if __name__ == "__main__":
    main()
