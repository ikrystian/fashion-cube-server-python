# seed.py
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime

from configs.mongo_config import db

# Seed categories
categories = [
    {"categoryName": "Basics"},
    {"categoryName": "Blazer"},
    {"categoryName": "Knitwear"},
    {"categoryName": "Jeans"},
    {"categoryName": "Jackets"},
    {"categoryName": "Girl"},
    {"categoryName": "Boy"}
]

# Seed departments
departments = [
    {"departmentName": "Women", "categories": "Basics,Blazer"},
    {"departmentName": "Men", "categories": "Knitwear,Jeans,Jackets"},
    {"departmentName": "Kids", "categories": "Girl,Boy"}
]

# Seed products
products = [
    {
        "imagePath": "https://static.zara.net/photos///2018/I/0/1/p/7568/644/802/2/w/1920/7568644802_1_1_1.jpg?ts=1541152091085",
        "title": "Oversized Textured Top",
        "description": "High collar top with short cuffed sleeves. Asymmetric hem with side slits.",
        "price": 35.95,
        "color": "Gray",
        "size": "XS,S,M",
        "quantity": 10,
        "department": "Women",
        "category": "Basics",
        "date": int(datetime(2020, 2, 12).timestamp() * 1000)  # Example date in milliseconds
    },
    {
        "imagePath": "https://static.zara.net/photos///2018/I/0/1/p/5644/641/800/2/w/1920/5644641800_2_5_1.jpg?ts=1540395699528",
        "title": "Tank Top",
        "description": "Flowy V-neck camisole with spaghetti straps.",
        "price": 29.99,
        "color": "Black",
        "size": "XS,S,XL",
        "quantity": 15,
        "department": "Women",
        "category": "Basics",
        "date": int(datetime(2020, 8, 17).timestamp() * 1000)
    },
    # Add more products as needed
]

# Seed variants
variants = [
    {
        "productID": "5bedf31cc14d7822b39d9d43",
        "imagePath": "https://static.zara.net/photos///2018/I/0/1/p/7568/644/710/2/w/1920/7568644710_1_1_1.jpg?ts=1541151891840",
        "color": "Beige",
        "size": "S,L",
        "quantity": 5,
    },
    {
        "productID": "5bedf3b9c14d7822b39d9d45",
        "imagePath": "https://static.zara.net/photos///2018/I/0/1/p/5644/641/735/2/w/1920/5644641735_2_5_1.jpg?ts=1540395590656",
        "color": "Copper",
        "size": "S,L,XL",
        "quantity": 12,
    },
    # Add more variants as needed
]

user = {
   "username": 'admin@admin.com',
   "password": 'admin',
   "fullname": 'Krystian Celebican',
   "admin": True
}

# Insert data into the database
def seed_database():
    db.categories.delete_many({})
    db.departments.delete_many({})
    db.products.delete_many({})
    db.variants.delete_many({})

    # Insert categories
    db.categories.insert_many(categories)
    print("Categories seeded.")

    # Insert departments
    db.departments.insert_many(departments)
    print("Departments seeded.")

    # Insert products
    db.products.insert_many(products)
    print("Products seeded.")

    # Insert variants
    db.variants.insert_many(variants)
    print("Variants seeded.")

    db.users.insert_one(user)
    print("Users seeded")

if __name__ == "__main__":
    seed_database()