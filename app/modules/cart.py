# app/modules/cart.py
from app.models.cart import Cart as CartModel, CartItem
from app.database import get_db
from bson import ObjectId

class Cart:
    def __init__(self, cart_data=None):
        if cart_data:
            self.items = cart_data.get("items", {})
            self.totalQty = cart_data.get("totalQty", 0)
            self.totalPrice = cart_data.get("totalPrice", 0.0)
            self.userId = cart_data.get("userId", "")
        else:
            self.items = {}
            self.totalQty = 0
            self.totalPrice = 0.0
            self.userId = ""

    def add(self, item: CartItem, item_id: str):
        if item_id in self.items:
            self.items[item_id].qty += item.qty
            self.items[item_id].price += item.price
        else:
            self.items[item_id] = item
        self.totalQty += item.qty
        self.totalPrice += item.price

    def decrease_qty(self, item_id: str):
        if item_id in self.items:
            self.items[item_id].qty -= 1
            self.items[item_id].price -= self.items[item_id].item['price']
            self.totalQty -= 1
            self.totalPrice -= self.items[item_id].item['price']
            if self.items[item_id].qty <= 0:
                del self.items[item_id]

    def increase_qty(self, item_id: str):
        if item_id in self.items:
            self.items[item_id].qty += 1
            self.items[item_id].price += self.items[item_id].item['price']
            self.totalQty += 1
            self.totalPrice += self.items[item_id].item['price']

    def generate_model(self):
        return CartModel(
            items=self.items,
            totalQty=self.totalQty,
            totalPrice=self.totalPrice,
            userId=self.userId
        )

    @staticmethod
    async def get_cart_by_user_id(user_id: str):
        db = get_db()
        cart_data = await db.carts.find_one({"userId": user_id})
        return cart_data

    @staticmethod
    async def update_cart_by_user_id(user_id: str, cart_data: CartModel):
        db = get_db()
        updated_cart = await db.carts.find_one_and_update(
            {"userId": user_id},
            {"$set": cart_data.dict()},
            return_document=True
        )
        return updated_cart

    @staticmethod
    async def create_cart(cart_data: CartModel):
        db = get_db()
        cart = await db.carts.insert_one(cart_data.dict())
        return cart_data