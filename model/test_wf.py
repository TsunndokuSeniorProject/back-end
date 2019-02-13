from word_feature import word_feature
import nltk

wf = word_feature()

review = "\nI know who you are.\nThose five simple words\u2014forming a single ominous line in a note, taped to a front door\u2014set the tone.  Thomas Christopher Greene draws readers in with a compulsively readable and magnificently manipulative storyline that teeters on the rudimentary line drawn between literary and contemporary fiction. This being the third of his books I\u2019ve read and what I would consider the darkest and most suspense-heavy yet.Max and Susannah\u2014along with her fifteen-year-old son\u2014have relocated to a small town in Vermont. Making a name for himself in the art world has afforded Max opportunities, the biggest being a professorship and the use of a gorgeous home for his family. Flying high in their new glossy life, thrown off-course when they're hit with the turbulence the note's insinuation creates. Anxiety rampant, and desperation to keep things under wraps, leads to some morally questionable moves. Just as Max relaxes, thinking he handled the situation, another note pops up, followed by a third. The short chapters, twist riddled plot and engaging flow of the author\u2019s words set a frantic pace. Although, not every twist is what I would call unpredictable. In fact, readers are made privy to some of the foreseeable decisions\u2014unpredictably replaced by gall. Part of the fun comes from the shock value Max\u2019s despicable actions lend to the story and the ease in which he manages to justifies them. Readers are led to contemplate, who of the two\u2014Max or Susannah\u2014is the perfect liar? Is it the dutiful wife who, despite her misgivings, stands by her husband\u2019s side? Or, is it the husband willing to go to any length to keep his secrets from reaching the light of day? Chances are\u2014whichever side you land on\u2014you have no idea what\u2019s in store or who in fact will prove to be the best liar. Until the end that is. The most fitting descriptor for the conclusion: adjective, ten letters, 4 syllables\u2014un\u00b7ex\u00b7pect\u00b7ed. *Thank you to St. Martin\u2019s Press for providing a review copy in exchange for my honest thoughts."
# print review


word_feature, word_map, all_reviews_sentence = wf.create_word_feature_test_set(review)

all_reviews_sentence = " ".join(all_reviews_sentence)
# print all_reviews_sentence
print nltk.word_tokenize(all_reviews_sentence)