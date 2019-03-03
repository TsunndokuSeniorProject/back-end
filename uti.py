import model.text_processor as tp
import os
import json
import spacy
nlp = spacy.load('en_core_web_sm')
all_reviews = ""
genres = os.listdir("web_scraper/goodreads/novel/")
for genre in genres:
    books = os.listdir("web_scraper/goodreads/novel/{}/".format(genre))
    for book in books:
        with open("web_scraper/goodreads/novel/{}/{}".format(genre, book), "r") as fp:
            data = json.load(fp)
        for review in data["Reviews"]:
            all_reviews += review["Review"] + " "
        

sentences_list = tp.opinion_sentence_filter(tp.split_into_sentences(all_reviews))

sentences_list_filtered = []
print("done filter")
for sentence in sentences_list:
    doc = nlp(sentence)
    for entity in doc.ents:
        if entity.label_ is "PERSON":
            sentence = sentence.replace(entity.text, "<Character>")
            # print(entity.text, entity.label_)
        # elif entity.label_ is "ORG":
        #     sentence = sentence.replace(entity.text, "<Organization>")
    if "spoiler)[" not in sentence and "<Replace>" not in sentence:
        sentences_list_filtered.append(sentence)

print("done replace")
sentences_list_filtered = "\n".join(sentences_list_filtered)



with open("sentences_filtered.txt", "w", encoding="utf-8") as fp:
    fp.write(sentences_list_filtered)