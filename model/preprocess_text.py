import json
import imitation_of_oms
import re

text = ""

with open("review.json","r") as fp:
    data = json.load(fp)
    for review in data['Reviews']:
        text += review['Review'] + " "
    fp.close()

text = text.replace("\n"," ").replace(".",". ")
text = re.sub(r'[^\x00-\x7F]+','', text)
text = imitation_of_oms.preProcessing(text)

text = imitation_of_oms.tokenizeReviews(text)

c = imitation_of_oms.posTagging(text)

d = imitation_of_oms.aspectExtraction(c)
from pprint import pprint
pprint(imitation_of_oms.identifyOpinionWords(c, d))