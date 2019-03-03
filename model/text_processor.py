# -*- coding: utf-8 -*-
import re
import nltk 
import spacy

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
    return sentences

def opinion_sentence_filter(splited_review):
    review_with_pos = []
    for sentence in splited_review:
        sentence_only_pos = ""
        sentence_pos = nltk.pos_tag(nltk.word_tokenize(sentence))
        for sp in sentence_pos:
            sentence_only_pos += str(sp[1])+" "
        review_with_pos.append([sentence,sentence_only_pos.strip()])
    opinion_sentences = []
    for review in review_with_pos:
        if "JJ" in review[1] or "RB" in review[1]:
            opinion_sentences.append(review[0])
    return opinion_sentences

if __name__ == "__main__":

    test_review = "\"Read Harry Potter 5.5 !\" they said. \"It'll be fun!\" they said. \"Our childhood was built on Harry Potter!\" they said.WELL YOUR CHILDHOODS WERE ALL HORRIBLE. OMG WHAT IS THIS BOOK? WHAT IS THIS MESS I'M IN?? Excuse me, but that large salty lake where my life used to be is my tears. Yes, yes, this means I loved it. But SERIOUSLY. Nooooot okay. At the end there, especially, I couldn't put the audio down so I was wandering about my house in a blind daze listening instead.And because every human and their fluffy poodle has probably sensibly reviewed this book, BAH. I'm just going to make a list of things I loved and things I didn't. My Intense And Passionate LOVES:\u2022 Harry + Ginny = yes. I was dubious at first. Like I think romance is NOT JKR's strong point...plus when she gets to a romantic scene she ends the chapter. HHAHAH. ADORABLE. (Not that I minded, I just...I think she's not good at romance.) But omg, there was that moment after the Quidditch match??? YUP. You know what I'm talking about. Excuse me, my heart just ran around in circles screaming and shipping.\u2022 Hermione: I adore her, but...I gotta admit, she was a little bit too stuffy. BUT I STILL LOVE HER. I love her love for learning.\u2022 I also adore how sensible Ginny is. \u2022 Fred and George's joke shop gives life. Also death, probs, but liiiiife.\u2022 I am utterly in LOVE with the whole concept of Hogwarts. I mean, I think it's stupid that they have to write with a quill and ink (can't they just enchant the quill to write for them?) and they seem to get an excessive amount of homework, BUT. It's all so vivid and detailed and it literally feels like Hogwarts is A REAL PLACE. I totally get why people wail about their letters going missing. \u2022 Speaking of detail...me likey. I always felt inside the story.\u2022 Plus the audio book (narrated by Jim Dale) is GREAT. I totally recommend it. I think Hermione's voice had a tendency to sound like an insufferable goat, but I got used to it. Harry's voice was perfection. \u2022 I also particularly liked Harry in this book. I JUST LOVE HARRY. <3 He's snarky, but he's lost some of the angriness from bk 5. He's got snarky quips at the ready, but he's also intensely...good. Like he's just a really GOOD chap, who makes bad decisions but really means well. ZOMG. *flails about* He was definitely my favourite character in this book. \u2022 ALSO DUMBLEDORE WAS GREAT. I love Dumbledore and how he's always polite and kind and smiley. (view spoiler)[ CAN WE TALK A MINUT EHOW I'M NOT OKAY THAT HE'S DEAD?!??!?!? LIKE WHAT EVEN THE FLYING HECK OF BROOMS NEST TAILS. THAT DOESN'T MAKE SENSE. BUT IT SHOULDN'T. BECAUSE NOTHING MAKES SENSE. Dumbledore. no. Come baaaaaaaack. *breaks down into a mess* I am also intensely furious that his weakening himself to get the horcrux was useless. MAD. Okay? I AM MAD. Character deaths where they failed are the worst there are.  (hide spoiler)]My Intense and Passionate LOATHES:(Hhahahha...you ready for this?)\u2022 Okay so, question: WHY do they sometimes go places and buy food...and sometimes they just magic it? Like Mrs. Weasely magics onion soup out of nothing for Harry. But in the next chapter, Harry and Ron are peeling sprouts. LIKE WUT. This makes no sense to me. \u2022 Why didn't Dumbledore pour the evil potion on the ground instead of drinking it? Just wannna know...\u2022 How the FLYING FRIKKIN BROOMSTICKS can anyone possibly convince me Snape is still on the good side? Because I don't even care. He can go abra kadabra himself to Timbuktu and DIE THERE THANKS. There is no repentance after this. I don't even care what the \"reason\" is in book 7, but Harry: you are an idiot to name your kid after Snape. \u2022 I HOPE SNAPE DIES.\u2022 DID I MENTION MY HATE FOR SNAPE YET???????\u2022 Oh and another thing...I am so angry at Snape arghhhqqwqq.\u2022 Okay. Good now. I'm calm. Thank you. \u2022 HAHHAHHAHAHTE SNAPE.\u2022 Yes, I truly am calm this time. I'm good.\u2022 So. I also am fairly annoyed about Voldermort's (Tom Riddle) backstory. Because he read like he was straight out of a psychopath text book...which I found monstrously unimaginative. Attractive, calm, subtle bully, kleptomaniac, limited emotional reach, charmer, smooth...blah blah. Yes. I can just read a book about psychopaths and that's Voldey's description. I wish there'd been a little more ingenuity in there.\u2022 I really also dislike Ron. I KNOW. Travesty. But he's a bully! He was bullying first year's the whole time...turfing tem off chairs, scaring them, bossing them around, taking stuff off them in the name of \"prefect\". Like how is that good?? How is that okay??? I will not forgive Ron for all this. And also the fact that he's a downright BRUTE to Hermione. How can I ship them when he's so rude and demeaning to her?? I DON'T. Hermione deserves better. And I don't buy the \"She completes him by sorting him out\" because I think all humans should take responsibility for their actions. Hermione shouldn't HAVE to force Ron into a better person and be his conscious. AGH. \u2022 Not shipping that. ^^\u2022 Okay, I'm done. But just *whispers* I hate hate hate Snape. So basically YES, I had a fantastic time with this book. I loved the audio. I loved the story. I loved Harry and the world just feels so big and rich and visual. I get the intense fandom for this I DO GET IT. After being so angry and 1000% done in with book 3, I can successfully say I can't WAIT to read the last book now. And then watch all the movies. And then I'll finally be caught up, omg. Only took me like 10 years. "
    splited_review = split_into_sentences(test_review)
    # print(splited_review)
    result = opinion_sentence_filter(splited_review)
    print(len(result))