import requests
from bs4 import BeautifulSoup
import time

reviews = []

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
    x = soup.find_all("span",{"data-hook":"review-body"})
    
    for row in x:
        reviews.append(row.text)

for item in reviews:
    print item
    print "-------------------- next review -----------------------"