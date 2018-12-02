import os
import json
 
data_directory = "./web_scraper/novel/comments/"
with open('./web_scraper/novel/log_asin.json') as data:
    log_asin = json.load(data)

# get asin number from file nanme
for filename in os.listdir(data_directory):
    print("\"" + filename[7:-5] + "\",")

# compare number of passed, failed, and number of json downloaded
print(len(set(log_asin['Passed'])))

print(len(set(log_asin['Failed'])))

print(len(os.listdir(data_directory)))