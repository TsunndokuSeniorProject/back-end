import nltk
import ast
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('sentiwordnet')


class opinion_mining_system:

    def split_sentence(self, full_text_reviews):
        sentence_tokenize = nltk.tokenize.punkt.PunktSentenceTokenizer().tokenize(full_text_reviews)
        return sentence_tokenize
    
    def operate_aspect_extraction(self, full_text_reviews):
        sentence_list = self.split_sentence(full_text_reviews)
        sentence_pos_list = []
        for sentence in sentence_list:
            sentence_pos_list.append(nltk.pos_tag(nltk.word_tokenize(sentence)))
        prevWord = ""
        prevTag = ""
        currWord = ""
        aspectList = []
        outputDict = {}
        for sentence in sentence_pos_list:
            for word, tag in sentence:
                if(tag == "NN" or tag == "NNP"):
                    if(prevTag == "NN" or prevTag == "NNP"):
                        currWord= prevWord + ' ' + word
                    else:
                        aspectList.append(prevWord.upper())
                        currWord= word
                prevWord=currWord
                prevTag=tag
        #Eliminating aspect which has 1 or less count
        for aspect in aspectList:
                if(aspectList.count(aspect) > 1):
                        if(outputDict.keys() != aspect):
                                outputDict[aspect] = aspectList.count(aspect)
        outputAspect = sorted(outputDict.items(), key=lambda x: x[1],reverse = True)
        return outputAspect

if __name__ == "__main__":
    
    a = """I have to say, the most sensible reviews are those that doesn't say 10/10. It wasn't easy to rate it, I had to think long and hard about this one before I could give it a seemingly justified mark.Sadly, "Bird Box" is nothing revolutionary in neither the horror genre & the apocalyptical movie isle. It has a great cast, a truly great performance by Sandra Bullock, real good looking, big-budget-all-over cinematography, visual FX, shooting locations, action, makeup, etc., etc. Many aspects of a masterful filmmaking are on a high enough level - my only complaint on this matter is that there wasn't enough horror in this horror movie. A few moments of gore, mayhem and suspense fits the genre, but overall I'd describe "Bird Box" as an r-rated apocalyptical adventure movie that could easily have a lot of teenagers in it's audience. I'm seeing a lot comparisons with the recent "A Quiet Place" among the reviews, yet I'd like to try and avoid comparing these two, but, to all those who compare them, I say - "A Quiet Place" was a better horror movie (emphasis on "horror").
        So why only 6/10, you wonder? Let me tell you why: the plot. It is so lousy in so many ways. Note that I have not read the book, but if the story there is as unpolished as here, I will definitely never read it. "Bird Box" leaves the viewer with a lot of questions and plot points that doesn't make much sense. What are the entities? There are no origins, no explanation for how and why it struck the earth, it's shown as extremely powerful yet, for whatever reason, it can't enter any buildings etc. From the start of the movie to the end there is no development whatsoever regarding the reasons for the apocalypse and the process of it. Why are some people not killing themselves when exposed to the entities but are killing others? Well, I guess because they needed someone to kill the protagonists, when the entities couldn't.. There is never an explanation, not even a subtle hint. The entities can make you hear voices of close people, dead people, yet, 5 years into the apocalypse, it still comes as a surprise to the main charachters, what a climax, eh? In the end, after the long journey, our main character finds the place she was looking for - a school for the blind. In the middle of a rainforest. Very plausible indeed. Also, who calls their children girl and boy for 5 years, only to deliver the scene at the end where she names them after the two now dead charachters. I guess they had to wait until the father dies, otherwise there wouldn't be the sentimental reason to name the son after the father. Also, the character development is pretty predictable throughout the movie & the 2nd half gradually becomes more... generic.
        It might sound like I'm thrashing the movie, but, mind you, 6/10 is a good mark & I enjoyed this movie for its high entertainment value, but the depth here is shallow & the setting is an unpolished excuse for a story of a charachter's survival which brings almost nothing new to the cinematic history. An underwhelming yet entertaining thriller that will successfully reach a big audience for its too mainstream to be called anything other than a popcorn horror.
        The movie was OK. Definitely better than the Happening, and that's not saying much, but the Bird Box certainly did not live up to the hype. In a post-apocalyptic world where a supernatural entity is making people kill themselves once they see "it", Sandra Bullock's character must make it through the forest to a safe haven with two young children in tow, all while blindfolded - so she won't see "it". That's the premise and it's not too plausible. Walking through a dense forest blindfolded? Yeah, right. Hell, some people wouldn't be able to halfway walk through the woods without tripping over a log with full sight, yet we're expected to believe she can navigate blindfolded just fine with two children in tow?
        Anyway, we do get to see how Bullock's character got to this point via flashbacks, and quite frankly, those are the better parts of this movie. I think the best scene in Bird Box was when the initial survivors at the house in the city ran out of food and had to make a trip to the grocery store. Without giving away any details, this sequence is one of the few bright spots in terms of originality that you will see in this film.
        Besides that, we just see survivors surviving and then getting killed off and not much else. If you're looking for: who, what, why, or how? Good luck, you won't find "it" here. Otherwise, decent cinematography and acting by Sandra Bullock, John Malkovich, Trevante Rhodes, and the little girl are the only things holding this movie together. It's worth a look. 5 stars."""

    print(opinion_mining_system().operate_aspect_extraction(a))
