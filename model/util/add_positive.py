import json
import pprint
pos_dict = ""
neg_dict = ""

with open("positive_adj.json", 'r') as pos:
    pos_dict = json.load(pos)

with open("negative_adj.json", 'r') as neg:
    neg_dict = json.load(neg)


review = ""
data = ""
with open('../../web_scraper/novel/comments/review_006246616X.json', 'r') as fp:
    data = json.load(fp)
    for comment in data['Comment']:
        neg_score = 0
        pos_score = 0
        # print(comment['Review'])
        # review = review+comment['Review']
        # print(comment["Star"][0])
        rating = comment["Star"][0]
        if int(rating) > 3:
            comment["positivity"] = 1
        elif int(rating) < 3:
            comment["positivity"] = 0
        else:
            for adj in pos_dict['word']:
                if adj in comment['Review']:
                    pos_score = pos_score+1

            for adj in neg_dict['word']:
                if adj in comment['Review']:
                    neg_score = neg_score+1

            print(pos_score)
            print(neg_score)
            if pos_score > neg_score:
                comment["positivity"] = 1
            else:
                comment["positivity"] = 0

pprint.pprint(data)
with open('../../web_scraper/novel/comments/review_006246616X.json', 'w') as fp:
    json.dump(data, fp)
