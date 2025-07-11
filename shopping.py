from flask import Flask, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

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
        self.items = {}

    def add_item(self, product, quantity):
        if product.stock < quantity:
            return f"Not enough stock for {product.name}"
        self.items[product.id] = self.items.get(product.id, 0) + quantity
        product.stock -= quantity
        return f"Added {quantity} x {product.name} to cart."

    def view_cart(self, product_db):
        cart_details = []
        total = 0
        for pid, qty in self.items.items():
            product = product_db[pid]
            cost = qty * product.price
            cart_details.append({
                'product': product.name,
                'quantity': qty,
                'price': product.price,
                'cost': cost
            })
            total += cost
        return cart_details, total

    def checkout(self, product_db):
        cart_details, total = self.view_cart(product_db)
        order = Order(self.user, self.items.copy(), total)
        self.items.clear()
        return order.to_dict()

class Order:
    def __init__(self, user, items, total_amount):
        self.order_id = str(uuid.uuid4())
        self.user = user
        self.items = items
        self.total_amount = total_amount
        self.status = "Placed"
        self.created_at = datetime.now()

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "user": self.user.username,
            "total_amount": self.total_amount,
            "status": self.status,
            "created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class Shop:
    def __init__(self):
        self.products = {}
        self.users = {}

    def add_product(self, name, price, stock):
        p = Product(name, price, stock)
        self.products[p.id] = p
        return p

    def register_user(self, username):
        user = User(username)
        self.users[user.id] = user
        return user

# =============================
# Initialize Shop and Data
# =============================

flipkart = Shop()
p1 = flipkart.add_product("iPhone 14", 70000, 10)
p2 = flipkart.add_product("Samsung TV", 45000, 5)
p3 = flipkart.add_product("Sony Headphones", 3000, 20)
user1 = flipkart.register_user("sundar_123")

# =============================
# Flask Routes (Browser/API)
# =============================

@app.route('/')
def home():
    return "🛒 Shopping Cart App is running!"

@app.route('/add')
def add_items():
    result1 = user1.cart.add_item(p1, 1)
    result2 = user1.cart.add_item(p2, 1)
    return jsonify({"added": [result1, result2]})

@app.route('/cart')
def view_cart():
    items, total = user1.cart.view_cart(flipkart.products)
    return jsonify({"cart": items, "total": total})

@app.route('/checkout')
def checkout():
    order = user1.cart.checkout(flipkart.products)
    return jsonify({"order": order})

# =============================
# Run the App
# =============================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8070)
