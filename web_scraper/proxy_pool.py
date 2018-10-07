import requests
from bs4 import BeautifulSoup
import pandas as pd 
class Pool:

    def __init__(self):
        self.url = "https://free-proxy-list.net"

    def getProxy(self):
        proxy = []
        data = requests.get(self.url)
        if str(data.status_code) != "200":
            return proxy
        soup = BeautifulSoup(data.text, 'html.parser')
        table = soup.find_all("table", {"id": "proxylisttable"})
        tr = table[0].find_all("tr")
        for td in tr:
            t_data = td.find_all("td")
            if len(t_data) > 1:
                proxy.append(str(t_data[0].text)+":"+str(t_data[1].text))
        
        return proxy

if __name__ == "__main__":
    pool = Pool()
    print pool.getProxy()