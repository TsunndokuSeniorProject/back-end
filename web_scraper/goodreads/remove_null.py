import os
import json
genres = os.listdir("novel/")
for genre in genres:
    if genre != ".DS_Store":
        reviews = os.listdir("novel/{}/".format(genre))
        for review in reviews:
            if review != ".DS_Store":
                with open("novel/{}/{}".format(genre, review), "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                if data is None: 
                    print("novel/{}/{}".format(genre, review))
                    os.remove("novel/{}/{}".format(genre, review))
