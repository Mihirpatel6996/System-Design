from typing import List

from models.user import User
from models.restaurant import Restaurant
from models.menu_items import MenuItem
from models.cart import Cart
from models.orders import Order

from managers.restaurant_manager import RestaurantManager
from managers.order_manager import OrderManager

from strategies.payment_strategy import PaymentStrategy

from factories.now_order_factory import NowOrderFactory
from factories.scheduled_order_factory import ScheduledOrderFactory
from factories.order_factory import OrderFactory

from services.notification_service import NotificationService


class TomatoApp:
    """
    Facade / Orchestrator for the entire system.

    Simulates:
    - API layer
    - User interactions
    """

    def __init__(self):
        self.initialize_restaurants()

    # ---------------- Setup ----------------

    def initialize_restaurants(self) -> None:
        r1 = Restaurant("Bikaner", "Delhi")
        r1.add_menu_item(MenuItem("P1", "Chole Bhature", 120))
        r1.add_menu_item(MenuItem("P2", "Samosa", 15))

        r2 = Restaurant("Haldiram", "Kolkata")
        r2.add_menu_item(MenuItem("P1", "Raj Kachori", 80))
        r2.add_menu_item(MenuItem("P2", "Pav Bhaji", 100))
        r2.add_menu_item(MenuItem("P3", "Dhokla", 50))

        r3 = Restaurant("Saravana Bhavan", "Chennai")
        r3.add_menu_item(MenuItem("P1", "Masala Dosa", 90))
        r3.add_menu_item(MenuItem("P2", "Idli Vada", 60))
        r3.add_menu_item(MenuItem("P3", "Filter Coffee", 30))

        rm = RestaurantManager.get_instance()
        rm.add_restaurant(r1)
        rm.add_restaurant(r2)
        rm.add_restaurant(r3)

    # ---------------- Search ----------------

    def search_restaurants(self, location: str) -> List[Restaurant]:
        return RestaurantManager.get_instance().search_by_location(location)

    # ---------------- Cart Operations ----------------

    def select_restaurant(self, user: User, restaurant: Restaurant) -> None:
        user.get_cart().set_restaurant(restaurant)

    def add_to_cart(self, user: User, item_code: str) -> None:
        cart = user.get_cart()
        restaurant = cart.get_restaurant()

        if restaurant is None:
            print("Please select a restaurant first.")
            return

        for item in restaurant.get_menu():
            if item.get_code() == item_code:
                cart.add_item(item)
                return

        print("Item not found.")

    # ---------------- Checkout ----------------

    def checkout_now(self, user: User, order_type: str, payment_strategy: PaymentStrategy) -> Order:
        return self._checkout(user, order_type, payment_strategy, NowOrderFactory())

    def checkout_scheduled(
        self,
        user: User,
        order_type: str,
        payment_strategy: PaymentStrategy,
        schedule_time: str
    ) -> Order:
        return self._checkout(
            user,
            order_type,
            payment_strategy,
            ScheduledOrderFactory(schedule_time)
        )

    def _checkout(
        self,
        user: User,
        order_type: str,
        payment_strategy: PaymentStrategy,
        factory: OrderFactory
    ) -> Order:

        cart = user.get_cart()

        if cart.is_empty():
            print("Cart is empty.")
            return None

        order = factory.create_order(
            user=user,
            cart=cart,
            restaurant=cart.get_restaurant(),
            items=cart.get_items(),
            payment_strategy=payment_strategy,
            order_type=order_type
        )

        OrderManager.get_instance().add_order(order)

        return order

    # ---------------- Payment ----------------

    def pay_for_order(self, user: User, order: Order) -> None:
        success = order.process_payment()

        if success:
            NotificationService.notify(order)
            user.get_cart().clear()
        else:
            print("Payment failed.")

    # ---------------- Debug ----------------

    def print_user_cart(self, user: User) -> None:
        cart = user.get_cart()

        print("Items in cart:")
        print("------------------------------------")

        for item in cart.get_items():
            print(f"{item.get_code()} : {item.get_name()} : ₹{item.get_price()}")

        print("------------------------------------")
        print(f"Grand total : ₹{cart.get_total_cost()}")