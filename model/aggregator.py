import pandas as pd

def compute_score(aspect_list, polarity_list):
    story_score = [0,0,0]
    story_score_dict = {}
    writing_score = [0,0,0]
    writing_score_dict = {}
    char_score = [0,0,0]
    char_score_dict = {}
    total_story = 0
    total_writing = 0
    total_char = 0
    for asp, senti in zip(aspect_list, polarity_list):
        # print(senti)
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
        story_score_dict["neutral"] = story_score[0]/total_story
        story_score_dict["positive"] = story_score[1]/total_story
        story_score_dict["negative"] = story_score[2]/total_story

    except ZeroDivisionError:
        pass
    try:
        writing_score_dict["neutral"] = writing_score[0]/total_writing
        writing_score_dict["positive"] = writing_score[1]/total_writing
        writing_score_dict["negative"] = writing_score[2]/total_writing
    except ZeroDivisionError:
        pass
            
    try:
        char_score_dict["neutral"] = char_score[0]/total_char
        char_score_dict["positive"] = char_score[1]/total_char
        char_score_dict["negative"] = char_score[2]/total_char
    except ZeroDivisionError:
        pass
        
    res = {"story_score": {"score": story_score_dict, "sentence":None}, "writing_score": {"score": writing_score_dict, "sentence":None}, "char_score": {"score": char_score_dict, "sentence":None}}
    return res

def map_sentence(bea_list, aspect_list, polarity_list):
    bea_back = []
    asp_back = []
    polar_back = []
    
    for sen, asp, senti in zip(bea_list, aspect_list, polarity_list):
        temp_asp = list(set(asp))
        # print(asp)
        # print(temp_asp)
        for single in temp_asp:
            bea_back.append(sen)
            asp_back.append(single)
            polar_back.append(senti)

    return bea_back, asp_back, polar_back

def group_result(result_df):
    groups = result_df.groupby("aspect")
    story_df = []
    writing_df = []
    character_df = []
    for group in groups:
        if group[0] == 1:
            story_df = group[1]
        elif group[0] == 2:
            writing_df = group[1]
        elif group[0] == 3:
            character_df = group[1]
    

    pos_story_rec = []
    neg_story_rec = []
    neu_story_rec = []
    if type(story_df) is not list:
        story_df = story_df.groupby("polarity")
        for po in story_df:
            if po[0] == 1:
                pos_story_rec = po[1].to_dict("records")
            elif po[0] == 2:
                neg_story_rec = po[1].to_dict("records")
            elif po[0] == 0:
                neu_story_rec = po[1].to_dict("records")

    pos_writing_rec = []
    neg_writing_rec = []
    neu_writing_rec = []
    if type(writing_df) is not list:
        writing_df = writing_df.groupby("polarity")
        for po in writing_df:
            if po[0] == 1:
                pos_writing_rec = po[1].to_dict("records")
            elif po[0] == 2:
                neg_writing_rec = po[1].to_dict("records")
            elif po[0] == 0:
                neu_writing_rec = po[1].to_dict("records")

    pos_character_rec = []
    neg_character_rec = []
    neu_character_rec = []
    if type(character_df) is not list:
        character_df = character_df.groupby("polarity")
        for po in character_df:
            if po[0] == 1:
                pos_character_rec = po[1].to_dict("records")
            elif po[0] == 2:
                neg_character_rec = po[1].to_dict("records")
            elif po[0] == 0:
                neu_character_rec = po[1].to_dict("records")

    return pos_story_rec, neg_story_rec, neu_story_rec, pos_writing_rec, neg_writing_rec, neu_writing_rec, pos_character_rec, neg_character_rec, neu_character_rec