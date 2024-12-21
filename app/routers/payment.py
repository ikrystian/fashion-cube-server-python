# app/routers/payment.py
from fastapi import APIRouter, HTTPException, Depends
from app.models.order import Order
from app.database import get_db
from app.modules.ensure_authenticated import ensure_authenticated
from app.models.user import User  # Import the User model

router = APIRouter()

@router.post("/")
async def payment_success(order_id: str, current_user: User = Depends(ensure_authenticated)):
    db = get_db()

    # Fetch the order from the database
    order = await db.orders.find_one({"_id": order_id, "userId": current_user.id})

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Update the order status to 'paid' or similar
    updated_order = await db.orders.find_one_and_update(
        {"_id": order_id},
        {"$set": {"status": "paid"}},
        return_document=True
    )

    if not updated_order:
        raise HTTPException(status_code=500, detail="Failed to update order status")

    return {"message": "Payment successful", "order_id": order_id}