from typing import List

from models.orders import Order
from models.menu_items import MenuItem


class NotificationService:
    """
    Handles notifications for orders.

    In real systems:
    - SMS
    - Email
    - Push notifications
    """

    @staticmethod
    def notify(order: Order) -> None:
        print("\nNotification: New order placed!")
        print("---------------------------------------------")

        user = order.get_user()
        restaurant = order.get_restaurant()

        print(f"Order ID: {order.get_order_id()}")
        print(f"Customer: {user.get_name() if user else 'Unknown'}")
        print(f"Restaurant: {restaurant.get_name() if restaurant else 'Unknown'}")

        print("Items Ordered:")
        items: List[MenuItem] = order.get_items()

        for item in items:
            print(f"   - {item.get_name()} (₹{item.get_price()})")

        print(f"Total: ₹{order.get_total()}")
        print(f"Scheduled For: {order.get_scheduled()}")
        print("Payment: Done")

        print("---------------------------------------------")