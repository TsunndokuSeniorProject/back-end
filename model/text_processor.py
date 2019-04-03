# -*- coding: utf-8 -*-
import re
import nltk 
import spacy

def filter_english(sentence_list):
    filtered_sentence_list = []
    for sentence in sentence_list:
        if re.search(r'[^\x00-\x7F]+', sentence) == None:
            filtered_sentence_list.append(sentence)
    return filtered_sentence_list

def split_into_sentences(text):
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

def opinion_sentence_filter(splited_review):
    review_with_pos = []
    for sentence in splited_review:
        ufo_lang = re.search(r'[^\x00-\x7F]+', sentence)
        if ufo_lang is None:
            sentence_only_pos = ""
            sentence_pos = nltk.pos_tag(nltk.word_tokenize(sentence))
            for sp in sentence_pos:
                sentence_only_pos += str(sp[1])+" "
            review_with_pos.append([sentence,sentence_only_pos.strip()])
    opinion_sentences = []
    un_opinion = []
    for review in review_with_pos:
        if "JJ" in review[1] or "RB" in review[1]:
            opinion_sentences.append(review[0])
        else:
            un_opinion.append(review[0])
    print("filter sentences {}".format(len(opinion_sentences)))
    print("filter out sentences {}".format(len(un_opinion)))
    return opinion_sentences

def split_phrase(text):
    temp = []
    if "," in text:
        phrases = text.split(",")
        num_phrase = len(phrases)
        for i in range(0, num_phrase):
            temp.append(str(",".join(phrases[:i])) + "\n") 
        temp.append(text + "\n")
        temp.reverse()
    else:
        temp.append(text)
    return "".join(temp)
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
    with open("data.txt", "r", encoding="utf-8") as fp:
        data = fp.readlines()

        fp.close()

    print(filter_english(data))