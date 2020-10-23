import re
import sys
import math
import random
import json
from pprint import pprint
from collections import OrderedDict

def splitData(filepath):

    with open(filepath) as file:
        data = file.read()

    data = data.split('\n')

    del data[-1]

    return data

def tokenData(data):

    tokenList = []

    for review in data:
        r = review.split()
        del r[0]

        tokenList.append(r)
    
    return tokenList


def notHandling(data):

    notHandlingFlag = False

    for review in data:
        for x in range(len(review)):
            
            specialMatch = re.match(r"""[()-,?\/:'"|]""", review[x])

            if review[x] == "." and notHandlingFlag:
                notHandlingFlag = False
            elif notHandlingFlag and not specialMatch:
                review[x] = "not_{}".format(review[x])

            if review[x] == "not":
                notHandlingFlag = True
            
    return data

def bundleData(data):

    reviews = {"pos": [], "neg": []}

    for token in data:
        if(token[0]) == '0':
            del token[0]
            reviews["neg"].append(token)
        else:
            del token[0]
            reviews["pos"].append(token)

    return reviews
            


def getNgramCounts(data):

    ngramCount = {"pos": {}, "neg": {}}

    for key, review in data.items():
        for tokens in review:
            for token in tokens:
                if token not in ngramCount[key]:
                    ngramCount[key][token] = 1
                else:
                    ngramCount[key][token] += 1

    return ngramCount


def classify(wordList, ngrams):

    positive = ngrams['pos']
    negative = ngrams['neg']

    result = {}

    for word in wordList:

        if word not in positive:
            result[word] = 0
            continue

        if word not in negative:
            result[word] = 1
            continue
        
        if(positive[word] > negative[word]):
            result[word] = 1
        elif (positive[word] < negative[word]):
            result[word] = 0
        else:
            result[word] = random.randint(0, 1)
    
    return result

def countLength(id, ngrams):

    count = 0

    for word, vale in ngrams[id].items():
        count += vale

    return count


def createDiscussionList(ngrams, review, posVocabLength, negVocabLength, reviewVocabLength, masterClassified):

    positive = ngrams['pos']
    negative = ngrams['neg']

    discussionList = {}

    for word in review:
        
        if word in positive:
            x = ngrams["pos"][word] + 1
        else: 
            x = 1

        if word in negative:
            y = ngrams["neg"][word] + 1
        else:
            y = 1

        p = (x / (posVocabLength + abs(reviewVocabLength)))
        p1 = (y / (negVocabLength + abs(reviewVocabLength)))
        
        value = abs(math.log2(p/p1))

        discussionList[word] = {"val": value, "class": masterClassified[word]}

    return discussionList

def writeListToFile(discussionList):

    sortedDiscussionList = sorted(discussionList.items(), key=lambda x: x[1]["val"], reverse=True)

    with open("sentiment-decision-list.txt", "w") as filename:
        json.dump(sortedDiscussionList, filename, indent=4)


def preProcess(filepath):

    result = None

    split = splitData(filepath)
    tokens = tokenData(split)
    notHandlingData = notHandling(tokens)
    result = notHandlingData

    return result
        
def main(filepath):

    processedData = preProcess(filepath)

    classifiedData = bundleData(processedData)
    ngrams = getNgramCounts(classifiedData)

    posVocab = list(ngrams['pos'].keys())
    negVocab = list(ngrams['neg'].keys())
    reviewVocab = list(set(posVocab).union(negVocab))

    posVocabLength = countLength("pos", ngrams)
    negVocabLength = countLength("neg", ngrams)

    reviewVocabLength = len(reviewVocab)

    masterClassified = classify(reviewVocab, ngrams)

    disList = createDiscussionList(ngrams, reviewVocab, posVocabLength, negVocabLength, reviewVocabLength, masterClassified)

    writeListToFile(disList)


if __name__ == "__main__":

    filepath = sys.argv[1]

    main(filepath)
