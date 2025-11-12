from datetime import datetime
from typing import List

from .person import User
from .product import Candy
from .payment import PaymentMethod


class CartItem:
    """Represents a candy in the cart."""
    
    def __init__(self, candy: Candy, quantity: int):
        self.candy = candy
        self.quantity = quantity

    def subtotal(self):
        """Calculate the subtotal for this cart item."""
        return self.candy.price * self.quantity


class ShoppingCart:
    """User's temporary basket."""
    
    def __init__(self, user: User):
        self.user = user
        self._items: dict[Candy, CartItem] = {}  # Candy -> CartItem mapping for an efficient & faster search

    def add_item(self, candy: Candy, quantity: int):
        """Add candy to the shopping cart more efficiently."""
        if candy in self._items:
            self._items[candy].quantity += quantity
        else:
            self._items[candy] = CartItem(candy, quantity)

    def calculate_total(self):
        """Calculate the total amount in the cart."""
        return sum(item.subtotal() for item in self._items.values())

    def create_order(self, payment_method: PaymentMethod) -> "Order":
        """Create an order from the current cart contents."""
        total = self.calculate_total()
        order_items = [OrderItem(i.candy, i.quantity) for i in self._items.values()]
        return Order(self.user, order_items, total, payment_method)

    def clear(self):
        """Clear all items from the cart."""
        self._items.clear()

    def get_items(self) -> List[CartItem]:
        """Get a copy of the cart items."""
        return list(self._items.values())


class Order:
    """Represents a confirmed order."""
    
    order_counter = 1000

    def __init__(self, user: User, items: List["OrderItem"], total_amount: float, payment_method: PaymentMethod):
        self.order_id = Order.order_counter
        Order.order_counter += 1
        self.user = user
        self.items = items
        self.total_amount = total_amount
        self.payment_method = payment_method
        self.status = "Pending"
        self.timestamp = datetime.now()

    def confirm_payment(self):
        """Process payment and mark the order as paid."""
        if self.payment_method.process_payment(self.total_amount):
            self.status = "Paid"
            return True
        else:
            self.status = "Payment Failed"
            return False

    def ship_order(self):
        """Mark the order as shipped."""
        self.status = "Shipped"


class OrderItem:
    """A candy included in an order."""
    
    def __init__(self, candy: Candy, quantity: int):
        self.candy = candy
        self.quantity = quantity
        self.subtotal = candy.price * quantity
