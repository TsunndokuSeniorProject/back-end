import os
import json
import scraper
import time
genres = os.listdir("novel/")
count = []


for genre in genres:
    if genre != ".DS_Store":
        reviews = os.listdir("novel/{}/".format(genre))
        for review in reviews:
            if review != ".DS_Store":
                with open("memo_2.json", "r", encoding="utf-8") as fp:
                    memo = json.load(fp)
                    fp.close()
                with open("novel/{}/{}".format(genre, review), "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    fp.close()
                if "Author" in data and "ISBN" not in data:
                    memo.remove(data["ID"])
                if data["ID"] not in memo["book"]:
                    print(data["ID"])
                    try:
                        author, isbn = scraper.get_book_info_google(data["Name"])
                        data["Author"] = author
                        data["ISBN"] = isbn
                        with open("novel/{}/{}".format(genre, review), "w", encoding="utf-8") as fp:
                            json.dump(data ,fp)
                            fp.close()
                        # if data is None: 
                        #     print("novel/{}/{}".format(genre, review))
                        #     count.append("novel/{}/{}".format(genre, review))
                            # os.remove("novel/{}/{}".format(genre, review))
                        memo["book"].append(data["ID"])
                        with open("memo_2.json", "w", encoding="utf-8") as fp:
                            json.dump(memo ,fp)
                            fp.close()
                        time.sleep(4)
                    except:
                        print("pause")
                        time.sleep(240)
# print(len(count))