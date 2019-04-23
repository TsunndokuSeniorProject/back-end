# import model.text_processor as tp
# import os
# import json
# # import spacy
# nlp = spacy.load('en_core_web_sm')
# all_reviews = ""
# genres = os.listdir("web_scraper/goodreads/novel/")
# for genre in genres:
#     books = os.listdir("web_scraper/goodreads/novel/{}/".format(genre))
#     print(genre)
#     for book in books:
#         # print(book)
#         with open("web_scraper/goodreads/novel/{}/{}".format(genre, book), "r") as fp:
#             data = json.load(fp)
#         book_name = data["Name"]
#         author = data["Author"]
#         for review in data["Reviews"]:
#             all_reviews += review["Review"].replace(book_name, "bookname") + " "
#     #         break
#     #     break
#     # break


# #     all_reviews += " {} is good.".format(genre)

# # genres = ["classics", "romance", "young" "adult", "mystery", "horror", "historical", "humor", "nonfiction", "thriller", "fiction", "crime", "science fiction", "fantasy"]        

# # for genre in genres:
# #     if " {} is good.".format(genre) in all_reviews:
# #         print("{}, True".format(genre))
# sentences_list = tp.filter_english(tp.split_into_sentences_regex(all_reviews))

# sentences_list_filtered = sentences_list

# print("done filter")
# # for genre in genres:
# #     if " {} is good.".format(genre) in all_reviews:
# #         print("{}, True".format(genre))
# # for sentence in sentences_list:

# #     doc = nlp(sentence)

# #     for entity in doc.ents:
# #         if entity.label_ is "PERSON":
# #             sentence = sentence.replace(entity.text, "imp_char")
# #             # print(entity.text, entity.label_)
# #         # elif entity.label_ is "ORG":
# #         #     sentence = sentence.replace(entity.text, "<Organization>")
# #     if "spoiler)[" not in sentence and "<Replace>" not in sentence:
# #         sentences_list_filtered.append(sentence)


# # print("done replace")
# # for genre in genres:
# #     if " {} is good.".format(genre) in all_reviews:
# #         print("{}, True".format(genre))
# sentences_list_filtered = "\n".join(sentences_list_filtered)

# # print(sentences_list_filtered)
# # print(len(sentences_list_filtered))
# with open("sentences_filtered.txt", "w+", encoding="utf-8") as fp:
#     fp.write(sentences_list_filtered)