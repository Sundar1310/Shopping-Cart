import uuid
from datetime import datetime

# =============================
# Data Classes and Structures
# =============================

class Product:
    def __init__(self, name, price, stock):
        self.id = str(uuid.uuid4())
        self.name = name
        self.price = price
        self.stock = stock

class User:
    def __init__(self, username):
        self.id = str(uuid.uuid4())
        self.username = username
        self.cart = ShoppingCart(self)

class ShoppingCart:
    def __init__(self, user):
        self.user = user
        self.items = {}  # product_id -> quantity

    def add_item(self, product, quantity):
        if product.stock < quantity:
            print(f"Not enough stock for {product.name}")
            return
        self.items[product.id] = self.items.get(product.id, 0) + quantity
        product.stock -= quantity
        print(f"Added {quantity} x {product.name} to cart.")

    def remove_item(self, product, quantity):
        if product.id not in self.items:
            print("Item not in cart.")
            return
        if quantity >= self.items[product.id]:
            quantity = self.items[product.id]
        self.items[product.id] -= quantity
        product.stock += quantity
        if self.items[product.id] == 0:
            del self.items[product.id]
        print(f"Removed {quantity} x {product.name} from cart.")

    def view_cart(self, product_db):
        print(f"\nCart for {self.user.username}:")
        total = 0
        for pid, qty in self.items.items():
            product = product_db[pid]
            cost = qty * product.price
            print(f"- {product.name}: {qty} x ₹{product.price} = ₹{cost}")
            total += cost
        print(f"Total: ₹{total}")
        return total

    def checkout(self, product_db):
        total = self.view_cart(product_db)
        print(f"\nProceeding to checkout... Total amount ₹{total}")
        order = Order(self.user, self.items.copy(), total)
        self.items.clear()
        return order


class Order:
    def __init__(self, user, items, total_amount):
        self.order_id = str(uuid.uuid4())
        self.user = user
        self.items = items
        self.total_amount = total_amount
        self.status = "Placed"
        self.created_at = datetime.now()
        print(f"✅ Order {self.order_id} placed successfully on {self.created_at}")


# =============================
# Mock Database
# =============================

class Shop:
    def __init__(self):
        self.products = {}  # id -> Product
        self.users = {}     # id -> User

    def add_product(self, name, price, stock):
        p = Product(name, price, stock)
        self.products[p.id] = p
        print(f"Added product: {name} | Price: ₹{price} | Stock: {stock}")
        return p

    def register_user(self, username):
        user = User(username)
        self.users[user.id] = user
        print(f"Registered user: {username}")
        return user


# =============================
# Simulation
# =============================

if __name__ == "__main__":
    flipkart = Shop()

    # Add products
    p1 = flipkart.add_product("iPhone 14", 70000, 10)
    p2 = flipkart.add_product("Samsung TV", 45000, 5)
    p3 = flipkart.add_product("Sony Headphones", 3000, 20)

    # Register user
    user1 = flipkart.register_user("sundar_123")

    # Add to cart
    user1.cart.add_item(p1, 1)
    user1.cart.add_item(p2, 1)
    user1.cart.view_cart(flipkart.products)

    # Checkout
    order = user1.cart.checkout(flipkart.products)
