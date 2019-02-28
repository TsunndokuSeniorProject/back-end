import sys
import json
import os
import pymongo
from pprint import pprint
import time
uri = "mongodb://tsundoku_db:tsundoku_db_007@ds133875.mlab.com:33875/tsundoku"

client = pymongo.MongoClient(uri)

db = client.get_default_database()

books = db['Books']

# start = time.time()
# query = books.find({"Genre":"/^{}$/i".format("crime")}).limit(50)
# que_time = time.time()
# for doc in query:
#     pprint(doc)
# print(start-que_time)


genres = os.listdir("web_scraper/goodreads/novel/")

for genre in genres:
    books_list = os.listdir("web_scraper/goodreads/novel/{}/".format(genre))
    for book in books_list:
        if book != ".DS_Store":
            with open("web_scraper/goodreads/novel/{}/{}".format(genre, book), "r") as fp:
                data = json.load(fp)
                data["_id"] = data["ID"]
            try:
                books.insert(data)
            except:
                continue