# app/routers/checkout.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.cart import Cart
from app.models.order import Order, create_order  # Import the create_order function
from app.modules.cart import Cart as CartModule
from app.modules.ensure_authenticated import ensure_authenticated
from app.models.user import User  # Import the User model

router = APIRouter()

@router.post("/{cart_id}")
async def checkout(cart_id: str, current_user: User = Depends(ensure_authenticated)):
    # Fetch the cart using the cart_id
    cart_data = await CartModule.get_cart_by_user_id(current_user.id)

    if not cart_data or cart_data.get("id") != cart_id:
        raise HTTPException(status_code=404, detail="Cart not found")

    # Calculate total amount and create an order
    total_amount = cart_data['totalPrice']

    # Create an order instance
    order = Order(
        userId=current_user.id,
        cartId=cart_id,
        totalAmount=total_amount,
        items=cart_data['items']
    )

    # Save the order to the database
    created_order = await create_order(order)

    # Optionally, clear the cart after checkout
    await CartModule.update_cart_by_user_id(current_user.id, Cart(items={}, totalQty=0, totalPrice=0, userId=current_user.id))

    return {"message": "Checkout successful", "order_id": str(created_order.id)}