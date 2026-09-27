from tomato_app import TomatoApp

from models.user import User
from strategies.upi_payment import UpiPaymentStrategy


def main():
    # ---------------- App Initialization ----------------
    tomato = TomatoApp()

    # ---------------- User Simulation ----------------
    user = User(101, "Aditya", "Delhi")
    print(f"User: {user.get_name()} is active.")

    # ---------------- Search Restaurants ----------------
    restaurant_list = tomato.search_restaurants("Delhi")

    if not restaurant_list:
        print("No restaurants found!")
        return

    print("Found Restaurants:")
    for restaurant in restaurant_list:
        print(f" - {restaurant.get_name()}")

    # ---------------- Select Restaurant ----------------
    selected_restaurant = restaurant_list[0]
    tomato.select_restaurant(user, selected_restaurant)

    print(f"Selected restaurant: {selected_restaurant.get_name()}")

    # ---------------- Add Items to Cart ----------------
    tomato.add_to_cart(user, "P1")
    tomato.add_to_cart(user, "P2")

    tomato.print_user_cart(user)

    # ---------------- Checkout ----------------
    order = tomato.checkout_now(
        user=user,
        order_type="Delivery",
        payment_strategy=UpiPaymentStrategy("1234567890")
    )

    # ---------------- Payment ----------------
    if order:
        tomato.pay_for_order(user, order)
    else:
        print("Checkout failed.")


if __name__ == "__main__":
    main()