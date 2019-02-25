import requests
from bs4 import BeautifulSoup
import json
import re
import os
import time

headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
        'Cache-Control': 'no-cache'
    } 

def get_id_by_genre(url):

    res = requests.get(url, headers=headers)

    soup = BeautifulSoup(res.text,"html.parser")

    book_id = [x["src"] for x in soup.find_all("img", {"class": "bookImage"})]

    image = [x.split("/")[-1] for x in book_id]

    book_id = [x.split(".")[0] for x in image]

    return book_id

def collect_id(url):
    book_id_list = []

    res = requests.get(url, headers=headers)
    if str(res.status_code) == "200":
        print(res.headers)
        print(url+" recieved")
        soup = BeautifulSoup(res.text,"html.parser")
        href = soup.find_all("a", {"class": "bookTitle"})
        
        id_pattern = re.compile("\d+")
        for link in href:
            print(link)
        for link in href:
            book_id = id_pattern.findall(str(link))
            if len(book_id) > 0:
                print("     "+book_id[0])
                book_id_list.append(book_id[0])
        
    else:
        print(url+" failed")
    # time.sleep(30)
    return book_id_list

def collect_id_from_file():
    soup = BeautifulSoup(open("html/"), "html.parser")


def get_book_reviews(book_id):
    print(book_id)
    res = requests.get("https://www.goodreads.com/book/show/"+book_id, headers=headers)
    if str(res.status_code) == "200":
        soup = BeautifulSoup(res.text,"html.parser")
        # Gather basic info
        try:
            desc = soup.find_all("div", {"id": "description"})
            desc = str(desc[0].find_all("span", {"id":re.compile("freeText\d+")})[0].text).strip()
        except:
            desc = "N/A"
        try:
            author = soup.find_all("span", {"itemprop": "name"})
            author = str(author[0].text).strip()
        except:
            author = "N/A"
        try:
            name = soup.find_all("h1", {"id": "bookTitle"})
            name = str(name[0].text).strip()
        except:
            name = "N/A"
        try:
            img = soup.find_all("img", {"id": "coverImage"})
            img = str(img[0]["src"])
        except:
            img = "N/A"
        try:
            genre = soup.find_all("a", {"class": "actionLinkLite bookPageGenreLink"})
            genre = str(genre[0].text).strip()
        except:
            genre = "N/A"
        book_reviews = {
            "Genre": genre,
            "ID": book_id,
            "Name": name,
            "Reviews":[],
            "Image":img,
            "Desc":desc
        }
        reviews = soup.find_all("div", {"class": "reviewText stacked"})
        for review in reviews:
            try:
                texts = review.find_all("span", {"id":re.compile("freeText\d+")})
                # texts = review.find_all("span", id=lambda value: value and value.startswith("freeText"))
                for text in texts:
                    book_reviews["Reviews"].append({"Review": text.text})
            except:
                pass

        return book_reviews
    else:
        return {"fail_message" : str(res.status_code)}

if __name__ == "__main__":
    ### don"t forget to change genre!!!
    # novel_id = get_id_by_genre("https://www.goodreads.com/genres/crime")
    # for book_id in novel_id:
    #     data = get_book_reviews(book_id)
    #     with open("novel/crime/review_"+str(book_id)+".json", "w+") as fp:
    #         json.dump(data, fp)
    #         fp.close()
    # novel = get_book_reviews("34019122")
    # import pprint
    # pprint.pprint(novel)


    book_id_list = []
    for page in range(1,3):
        book_id_list += collect_id("https://www.goodreads.com/shelf/show/crime?page="+str(page))

    book_id_list = list(set(book_id_list))
    print(book_id_list)
    # time.sleep(10)

    # print("all id "+str(len(book_id_list)))
    # for book_id in book_id_list:
    #     print("start "+book_id)
    #     data = get_book_reviews(book_id)
    #     print("get review "+book_id)
    #     path = "novel/"+str(data["Genre"]).lower()
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     print("genre "+str(data["Genre"]).lower())
    #     with open(path+"/review_"+str(book_id)+".json", "w+") as fp:
    #         json.dump(data, fp)
    #         fp.close()        
    #     print("done "+book_id)
