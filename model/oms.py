import nltk
import ast
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet
from file_reader import file_reader
import text_processor

class opinion_mining_system:
    
    # def operate_aspect_extraction(self, full_text_reviews):

    #     sentence_list = text_processor.split_into_sentences(full_text_reviews)
    #     sentence_list = text_processor.filter_english(sentence_list)
    #     print(sentence_list)
        # sentence_pos_list = []
        # for sentence in sentence_list:
        #     sentence_pos_list.append(nltk.pos_tag(nltk.word_tokenize(sentence)))
        # prevWord = ""
        # prevTag = ""
        # currWord = ""
        # aspectList = []
        # outputDict = {}
        # for sentence in sentence_pos_list:
        #     for word, tag in sentence:
        #         if(tag == "NN" or tag == "NNP"):
        #             if(prevTag == "NN" or prevTag == "NNP"):
        #                 currWord= prevWord + ' ' + word
        #             else:
        #                 aspectList.append(prevWord.upper())
        #                 currWord= word
        #         prevWord=currWord
        #         prevTag=tag
        # #Eliminating aspect which has 1 or less count
        # for aspect in aspectList:
        #         if(aspectList.count(aspect) > 1):
        #                 if(outputDict.keys() != aspect):
        #                         outputDict[aspect] = aspectList.count(aspect)
        # outputAspect = sorted(outputDict.items(), key=lambda x: x[1],reverse = True)
        # return outputAspect
        # return 0

    def operate_aspect_extraction(self, sentence_list):
        # sentence_list = text_processor.filter_english(text_processor.split_into_sentences(full_text_reviews))
        sentence_pos_list = []
        # print(len(sentence_list))
        for sentence in sentence_list:
            tagged_sen = nltk.pos_tag(nltk.word_tokenize(sentence))
            asp_sen = []
            for pos in tagged_sen:
                if "NN" in pos[1]:
                    asp_sen.append(pos[0])
            sentence_pos_list.append(asp_sen)
        print(len(sentence_pos_list))

        return sentence_pos_list

if __name__ == "__main__":
    
    a = """Listening to The Little imp_char brought back that sense of sadness and poignancy of reading this much loved story as a child.
    There is a great line in book_name about a book that has been abandoned in a garden The garden was deserted except for a red book which lay sunning itself upon the gravel path.
    The author then describes what the main characters are doing in various locations adjacent to the garden but meanwhile the red book is allowed to be caressed all the morning by the sun and to raise its covers slightly as though to acknowledge the caress.
    The description of the book seems very innocent but the reader s attention is immediately caught.
    What is the significance of this book within a book we wonder and why does it have a red cover.
    As it turns out the immediate purpose of the red covered book on that sunny English morning is to move the story along quickly and dramatically.
    The red book causes certain things to happen that wouldn t otherwise have happened as if it were in fact a character in the novel with a voice of its own.
    The plot is really very neat and makes for an entertaining read.
    The backdrops Forster uses for the action are interesting too the shifting class structure and the new ideas on religion and politics which were emerging in England in the last decades of the nineteenth century.
    But my favorite aspect of this beautiful novel is Art.
    Even when everything else is in flux Art is a constant and reliable reference which Forster returns to again and again.
    The first half of book_name takes place in Florence.
    The characters meet and avoid each other in a number of locations throughout the city at the Santa Croce church adorned with frescos by imp_char in the Piazza Della Signoria where imp_char stares across at Benvenuto Cellini s bloody imp_char under the Loggia dei Lanzi at the San Miniato church its beautiful facade visible from the very room of the title.
    Practically every scene in the Italian half of the book features some work of art or another directly or indirectly.
    When the characters take a trip into the hills landscape artists are recalled."""
    # s_l = file_reader().read("test.txt")
    print(opinion_mining_system().operate_aspect_extraction(a))
    # print(nltk.pos_tag(nltk.word_tokenize(a)))
