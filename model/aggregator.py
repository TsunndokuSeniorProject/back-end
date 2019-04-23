import pandas as pd

def compute_score(aspect_list, polarity_list):
    story_score = [0,0,0]
    writing_score = [0,0,0]
    char_score = [0,0,0]
    total_story = 0
    total_writing = 0
    total_char = 0
    for asp, senti in zip(aspect_list, polarity_list):
        print(senti)
        for single in asp:
            if single == 1:
                story_score[int(senti)] += 1
                total_story += 1
            elif single == 2:
                writing_score[int(senti)] += 1
                total_writing += 1
            elif single == 3:
                char_score[int(senti)] += 1
                total_char += 1

    try:
        story_score[0] = story_score[0]/total_story
        story_score[1] = story_score[1]/total_story
        story_score[2] = story_score[2]/total_story

    except ZeroDivisionError:
        pass
    try:
        writing_score[0] = writing_score[0]/total_writing
        writing_score[1] = writing_score[1]/total_writing
        writing_score[2] = writing_score[2]/total_writing
    except ZeroDivisionError:
        pass
            
    try:
        char_score[0] = char_score[0]/total_char
        char_score[1] = char_score[1]/total_char
        char_score[2] = char_score[2]/total_char
    except ZeroDivisionError:
        pass
        
    res = {"story_score": story_score, "writing_score": writing_score, "char_score": char_score}
    return res

def map_sentence(bea_list, aspect_list, polarity_list):
    bea_back = []
    asp_back = []
    polar_back = []
    for sen, asp, senti in zip(bea_list, list(set(aspect_list)), polarity_list):
        for single in asp:
            bea_back.append(sen)
            asp_back.append(single)
            polar_back.append(senti)

    return bea_back, asp_back, polar_back