import json
import os, os.path
import pprint
with open('dict.json') as data:
    dictionary = json.load(data)

directory = "../../web_scraper/novel/comments/"

# os.listdir("./path to comment")
books = [name for name in os.listdir(directory)]

comments = []
for book in books:
    with open(directory+book) as data:
        data = json.load(data)
    for comment in data['Comment']:
        comments = comments + comment['Review'].split('.')

story = []
character = []
telling = []
non_class = []

for key, value in dictionary.items():
    for v in value:
        count = 0
        for comment in comments:
            count = count + 1
            if count == len(comments)/2:
                break
            if v.lower() in comment.lower():

                # print(key)
                if key == "story":
                    story.append(comment)
                elif key == "character":
                    character.append(comment)
                elif key == "story_telling":
                    telling.append(comment)
            else:
                non_class.append(comment)

print(story)
with open("result.json", "w+") as write_out:
    json.dump({
        "story": story,
        "character": character,
        "telling": telling,
        "non_class": list(set(non_class))
    }, write_out)
# pprint.pprint(comments)
