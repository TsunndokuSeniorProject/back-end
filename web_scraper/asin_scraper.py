import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import time
import unicodedata

unique_asin = []

for page_num in range(1, 1000):

    url = "https://www.amazon.com/s/ref=sr_pg_2?fst=p90x%3A1&rh=n%3A283155%2Ck%3Anovel&page="+str(page_num)+"&keywords=novel"
    data = requests.get(url)
    print "Page number : "+str(page_num)
    print "Request status : "+str(data.status_code)

    if str(data.status_code) != "200":
        attempt = 1
        while str(data.status_code) != "200":
            print "wait for another attempt"
            time.sleep(5)
            url = "https://www.amazon.com/s/ref=sr_pg_2?fst=p90x%3A1&rh=n%3A283155%2Ck%3Anovel&page="+str(page_num)+"&keywords=novel"
            data = requests.get(url)
            print "Page number : "+str(page_num)+" #_Attempt : "+str(attempt)
            print "Request status : "+str(data.status_code)
            attempt += 1
    if "did not match any products" in data.text:
        print "No more book at "+str(page_num)
        break
    soup = BeautifulSoup(data.text,'html.parser')
    blogs = soup.find_all("li",{"id":re.compile("(result_\d+)")})

    for blog in blogs:
        title = blog.find_all("a",{"class":"a-link-normal s-access-detail-page s-color-twister-title-link a-text-normal"})
        if len(title) > 0:
            data_asin = u''.join(blog['data-asin']).encode('utf-8').strip()
            book_name = u''.join(title[0].text).encode('utf-8').strip()
            unique_asin.append([book_name, str(data_asin)])
    # break
    


table = pd.DataFrame(unique_asin, columns=['book_name', 'asin'])
table.drop_duplicates(subset=['asin'], keep='first', inplace=True)
table.to_csv("novel_asin_list.csv")