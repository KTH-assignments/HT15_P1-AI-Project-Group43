from nltk import *
from nltk.probability import *
from nltk.model import NgramModel
from nltk.corpus import treebank

if __name__ == '__main__':

    sentences = treebank.words()

    words = []
    for sentence in sentences:
        sent = word_tokenize(sentence)
        for s in sent:
            words.append(s)

    est = lambda fdist, bins: LidstoneProbDist(fdist, 0.2)
    langModel = NgramModel(4, words, estimator=est)

    conversation = ["", "", ""]
    while True:
        user = raw_input()
        conversation.append(user)
        last_three = conversation[-3:]
        predicted_word = langModel.generate(1, last_three)
        conversation.append(predicted_word[-1])
        print ' '.join(conversation)
