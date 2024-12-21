from pymongo import MongoClient

MONGO_HOSTNAME = '127.0.0.1'
MONGO_PORT = '27017'
MONGO_DB = 'fashion-cube'
client = MongoClient(f"mongodb://{MONGO_HOSTNAME}:{MONGO_PORT}/{MONGO_DB}")
db = client[MONGO_DB]