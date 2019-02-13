# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
from bs4 import BeautifulSoup
import json
import re
def get_id_by_genre(url):

    res = requests.get(url)

    soup = BeautifulSoup(res.text,'html.parser')

    book_id = [x['src'] for x in soup.find_all('img', {'class': 'bookImage'})]

    image = [x.split("/")[-1] for x in book_id]

    book_id = [x.split(".")[0] for x in image]

    return book_id


def get_book_reviews(book_id, genre):
    try:
        print book_id
        res = requests.get("https://www.goodreads.com/book/show/"+book_id)
        if str(res.status_code) == "200":
        
            soup = BeautifulSoup(res.text,'html.parser')

            img = soup.find_all('img', {'id': 'coverImage'})

            reviews = soup.find_all('div', {'class': 'reviewText stacked'})

            name = soup.find_all('h1', {'id': 'bookTitle'})

            desc = soup.find_all('div', {'id': 'description'})
            desc = ""
            try:
                desc = str(desc[0].find_all("span", {"id":re.compile("freeText\d+")})[0].text).strip()
            except:
                desc = ""
                print "no desc", sys.exc_info()[0]
            try:
                author = soup.find_all('span', {'itemprop': 'name'})
                name = str(name[0].text).strip()
                img = str(img[0]['src'])
                author = str(author[0].text).strip()
            except:
                author = ""
                name = ""
                img = ""
                author = ""
                print "no info", sys.exc_info()[0]
            book_reviews = {
                'Genre': genre,
                'ID': book_id,
                'Name': name,
                'Reviews':[],
                'Image':img,
                'Desc':desc
            }
            for review in reviews:
                try:
                    texts = review.find_all("span", {"id":re.compile("freeText\d+")})
                    # texts = review.find_all("span", id=lambda value: value and value.startswith("freeText"))
                    for text in texts:
                        book_reviews['Reviews'].append({"Review": text.text})
                except:
                    pass

            return book_reviews
    except:
        raise
        print "error ", sys.exc_info()[0]



### don't forget to change genre!!!

novel_id = get_id_by_genre('https://www.goodreads.com/genres/crime')

for book_id in novel_id:

    data = get_book_reviews(book_id, "Crime")

    with open('novel/crime/review_'+str(book_id)+'.json', 'w+') as fp:
        json.dump(data, fp)
        fp.close()