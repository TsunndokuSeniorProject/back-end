import requests
from bs4 import BeautifulSoup
import json
import re
def get_id_by_genre(url):

    res = requests.get(url)

    soup = BeautifulSoup(res.text,"html.parser")

    book_id = [x["src"] for x in soup.find_all("img", {"class": "bookImage"})]

    image = [x.split("/")[-1] for x in book_id]

    book_id = [x.split(".")[0] for x in image]

    return book_id


def get_book_reviews(book_id):
    print(book_id)
    res = requests.get("https://www.goodreads.com/book/show/"+book_id)
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
    novel = get_book_reviews("34019122")
    import pprint
    pprint.pprint(novel)