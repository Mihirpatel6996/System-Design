from factories.order_factory import OrderFactory
from models.delivery_order import DeliveryOrder
from models.pickup_order import PickupOrder
from models.orders import Order
from models.user import User
from models.cart import Cart
from models.restaurant import Restaurant
from strategies.payment_strategy import PaymentStrategy


class ScheduledOrderFactory(OrderFactory):
    """
    Creates scheduled orders.
    """

    def __init__(self, schedule_time: str):
        self._schedule_time = schedule_time

    def create_order(
        self,
        user: User,
        cart: Cart,
        restaurant: Restaurant,
        items,
        payment_strategy: PaymentStrategy,
        order_type: str
    ) -> Order:

        # --------- choose order type ---------
        if order_type.lower() == "delivery":
            order = DeliveryOrder()
            order.set_user_address(user.get_address())

        elif order_type.lower() == "pickup":
            order = PickupOrder()
            order.set_restaurant_address(restaurant.get_location())

        else:
            raise ValueError("Invalid order type")

        # --------- populate common fields ---------
        order.set_user(user)
        order.set_restaurant(restaurant)
        order.set_items(items)
        order.set_payment_strategy(payment_strategy)

        # scheduled time injected
        order.set_scheduled(self._schedule_time)

        return order