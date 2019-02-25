import sys
import pymongo

uri = "mongodb://tsundoku_db:tsundoku_db_007@ds133875.mlab.com:33875/tsundoku"

client = pymongo.MongoClient(uri)

db = client.get_default_database()

users = db['Users']


print(users.find_one({"name":"test"}))