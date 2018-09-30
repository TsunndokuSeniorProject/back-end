import requests
from bs4 import BeautifulSoup
import time
import re
reviews = []

book_info = None


for page_num in range(1, 1000):

    url = "https://www.amazon.com/product-reviews/B078XBQ4N5/ref=cm_cr_arp_d_paging_btm_"+str(page_num)+"?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(page_num) 
    data = requests.get(url)
    print "Page number : "+str(page_num)
    print "Request status : "+str(data.status_code)
    if "no reviews" in data.text:
        print "No more review at "+str(page_num)
        break
    soup = BeautifulSoup(data.text,'html.parser')
    # print(soup.prettify())
    if book_info is None:
        temp_soup = soup.find_all("div",{"role":"main"})
        book_info = {
            'Name':temp_soup[0].find_all("a",{"data-hook":"product-link"})[0].text,
            'Author':temp_soup[0].find_all("div",{"class":"a-row product-by-line"})[0].text.replace("by",""),
            'Price':temp_soup[0].find_all("span",{"class":"a-color-price arp-price"})[0].text,
            'Format':temp_soup[0].find_all("span",{"class":"a-size-base a-color-secondary"})[0].text,
            'Star':temp_soup[0].find_all("span",{"class":"arp-rating-out-of-text", "data-hook":"rating-out-of-text"})[0].text
        }

    review_section = soup.find_all("div",{"data-hook":"review"})
    for review in review_section:
        review_body = review.find_all("span",{"data-hook":"review-body"})
        upvote = review.find_all("span",{"data-hook":"helpful-vote-statement"})
        star = review.find_all("a",{"class":"a-link-normal", "title":re.compile("(\d+ out of \d+ stars)")})
        title = review.find_all("a",{"data-hook":"review-title"})
        # print len(star)
        # print star[0].text
        # print len(title)
        # print review_body[0].text
        # print upvote[0].text
        # print "------------"
        upvote = upvote[0].text
        upvote = re.search('(\d+)', upvote)
        upvote = 0 if upvote is None else upvote.group(0)
        reviews.append({
            'Review':review_body[0].text,
            'Upvote':upvote,
            'Title':title[0].text,
            'Star':star[0].text,
        })
    break
print book_info
print len(reviews)
for item in reviews:
    print item
    print "-------------------- next review -----------------------"