# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import requests
from bs4 import BeautifulSoup
import json

def get_id_by_genre(url):

    res = requests.get(url)

    soup = BeautifulSoup(res.text,'html.parser')

    book_id = [x['src'] for x in soup.find_all('img', {'class': 'bookImage'})]

    image = [x.split("/")[-1] for x in book_id]

    book_id = [x.split(".")[0] for x in image]

    return book_id


def get_book_reviews(book_id, genre):

    res = requests.get("https://www.goodreads.com/book/show/"+book_id)

    soup = BeautifulSoup(res.text,'html.parser')

    reviews = soup.find_all('div', {'class': 'reviewText stacked'})

    name = soup.find_all('h1', {'itemprop': 'name'})

    name = str(name[0].text).strip()
    book_reviews = {
        'Genre': genre,
        'ID': book_id,
        'Name': name,
        'Reviews':[]
    }

    for review in reviews:
        texts = review.find_all("span", id=lambda value: value and value.startswith("freeTextContainer"))
        for text in texts:
            book_reviews['Reviews'].append({"Review": text.text})

    return book_reviews



### don't forget to change genre!!!

novel_id = get_id_by_genre('https://www.goodreads.com/genres/romance')

for book_id in novel_id:

    data = get_book_reviews(book_id, "Romance")

    with open('novel/romance/review_'+str(book_id)+'.json', 'w+') as fp:
        json.dump(data, fp)
        fp.close()