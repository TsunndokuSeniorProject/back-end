import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import re
import pandas as pd
import json
from proxy_pool import Pool

exclude = []
with open('novel/log_asin.json', 'r') as fp:
    data = json.load(fp)
    exclude = data['Passed']

failed_req = []
passed_req = []
# Read all ASIN
asin_table = pd.read_csv('novel/novel_asin_list.csv')
asin_list = asin_table['asin'].tolist()

# Iterate over ASIN list
for asin in asin_list:
    if asin not in exclude:
        print "Asin : "+asin

        reviews = []

        book_info = None

        # Send request for comment review pages of each book
        for page_num in range(1, 100):
            isSkip = False
            url = "https://www.amazon.com/product-reviews/"+asin+"/ref=cm_cr_arp_d_paging_btm_"+str(page_num)+"?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(page_num) 
            data = requests.get(url)
            print "    Page number : "+str(page_num)
            print "    Request status : "+str(data.status_code)
            if str(data.status_code) != "200":
                attempt = 1
                while str(data.status_code) != "200":
                    print "    wait for another attempt"
                    print datetime.now()
                    time.sleep(900)
                    url = "https://www.amazon.com/s/ref=sr_pg_2?fst=p90x%3A1&rh=n%3A283155%2Ck%3Anovel&page="+str(page_num)+"&keywords=novel"
                    data = requests.get(url)
                    print "    Page number : "+str(page_num)+" #_Attempt : "+str(attempt)
                    print "    Request status : "+str(data.status_code)
                    if attempt > 5:
                        isSkip = True
                        break
                    attempt += 1

            # Skip to next ASIN if attempt > 5
            if isSkip:
                failed_req.append(asin)
                break
            if "no reviews" in data.text:
                print "No more review at "+str(page_num)
                break
            soup = BeautifulSoup(data.text,'html.parser')
            # print(soup.prettify())
            try:
                if book_info is None:
                    temp_soup = soup.find_all("div",{"role":"main"})
                    # print temp_soup[0].find_all("a",{"data-hook":"product-link", "class":"a-link-normal"})
                    book_info = {
                        'Name':temp_soup[0].find_all("a",{"data-hook":"product-link", "class":"a-link-normal"})[0].text,
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
                    upvote = upvote[0].text
                    upvote = re.search('(\d+)', upvote)
                    upvote = 0 if upvote is None else upvote.group(0)
                    reviews.append({
                        'Review':review_body[0].text,
                        'Upvote':upvote,
                        'Title':title[0].text,
                        'Star':star[0].text,
                    })
                passed_req.append(asin)
            except:
                failed_req.append(asin)
                break
            print datetime.now()
            time.sleep(180)
        log = {"Failed": [], "Passed": []}
        with open('novel/log_asin.json', 'r') as fp:
            log = json.load(fp)
            fp.close()   
        with open('novel/log_asin.json', 'w') as fp:
            json.dump({
                "Failed":log["Failed"]+failed_req,
                "Passed":log["Passed"]+passed_req
            }, fp)
            fp.close()
        if not book_info is None:   
            book_info['Comment'] = reviews
            with open('novel/comments/review_'+str(asin)+'.json', 'w') as fp:
                json.dump(book_info, fp)
                # fp.write(",\n")
                fp.close()
            time.sleep(900)
            print datetime.now()