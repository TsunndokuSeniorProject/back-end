# -*- coding: utf-8 -*-
import re
import nltk 
import spacy
import os
import json
# import spacy
# nlp = spacy.load('en_core_web_sm')
import en_core_web_sm
nlp = en_core_web_sm.load()
nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('sentiwordnet')

def filter_english(sentence_list):
    filtered_sentence_list = []
    for sentence in sentence_list:
        # if re.search(r'[^\u0000-\u007F]+', sentence) == None:
        sentence = re.sub(r'[^\u0041-\u005A | ^\u0061-\u007A]', " ", sentence)
        sentence = re.sub(r'\s+', " ", sentence)

        if sentence != " ":
            if "spoiler)[" not in sentence and "<Replace>" not in sentence:
                filtered_sentence_list.append(tag_character(sentence))
    return filtered_sentence_list

def replace_author(review, author="not available author"):
    name_surname = author.split(" ")
    review = review.replace(author, "authname")
    review = review.replace(name_surname[-1], "authname")
    review = review.replace(name_surname[0], "authname")
    return review

def replace_bookname(review, bookname="not available bookname"):
    title = bookname.split(" ")
    review = review.replace(bookname, "bookname")
    return review

def tag_character(sentence):
    
    doc = nlp(sentence)
    for entity in doc.ents:
        if entity.label_ is "PERSON":
            sentence = sentence.replace(entity.text, "impchar")
    return sentence.strip()

def split_into_sentences_regex(text):
    alphabets= "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|Mt)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|me|edu)"
    digits = "([0-9])"
    # text = text.lower()
    
    text = re.sub(r'\"(.+?)\"', "<Replace>", text)
    text = re.sub(r'\”(.+?)\”', "<Replace>", text)
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    
    if "”" in text:
        text = text.replace(".”","”.")
    if "\"" in text:
        text = text.replace(".\"","\".")
    if "!" in text:
        text = text.replace("!\"","\"!")
    if "?" in text:
        text = text.replace("?\"","\"?")
    if "..." in text:
        text = text.replace("...","<prd><prd><prd>")
    
    if "e.g." in text:
        text = text.replace("e.g.","e<prd>g<prd>") 
    if "i.e." in text:
        text = text.replace("i.e.","i<prd>e<prd>")
    text = text.replace("•","<stop>")
    text = text.replace(".","<stop>")
    text = text.replace("?","<stop>")
    text = text.replace("!","<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    print("split sentences {}".format(len(sentences)))
    return sentences

def split_into_sentences(text):
    sentence_tokenize = nltk.tokenize.punkt.PunktSentenceTokenizer().tokenize(text)
    return sentence_tokenize


if __name__ == "__main__":

    # source_file = "../sentences_filtered.txt"
    # fp = open(source_file, "r", encoding="utf-8")
    # new_content = ""
    # for line in fp.readlines():
    #     new_content += split_phrase(line)
    # fp.close()

    # fp = open("../new_sentences_filtered.txt", "w+", encoding="utf-8")
    # fp.write(new_content)
    # fp.close()
    text = ""
    genres = os.listdir("../web_scraper/goodreads/novel/")
    for genre in genres:
        if genre != ".DS_Store":
            novels = os.listdir("../web_scraper/goodreads/novel/{}/".format(genre))
            for novel in novels:
                if novel != ".DS_Store":
                    with open("../web_scraper/goodreads/novel/{}/{}".format(genre, novel), "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                    for review in data["Reviews"]:
                        text += review["Review"]+" "

    # with open("un_english_text.txt", "r", encoding="utf-8") as fp:
    #     data = fp.readlines()

    #     fp.close()

    processed_text = "\n".join(filter_english(split_into_sentences_regex(text)))
    
    with open("processed_text.txt", "w+", encoding="utf-8") as fp:
        fp.write(processed_text)
