import sys
import json
import re

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
        del r[1]

        tokenList.append(r)
    
    return tokenList


def notHandling(data):

    notHandlingFlag = False

    for review in data:
        for x in range(len(review)):
            
            specialMatch = re.match(r"""[()!-,?\/:'"|]""", review[x])

            endSentenceMatch = re.match(r'[.!?]', review[x])

            if endSentenceMatch and notHandlingFlag:
                notHandlingFlag = False
            elif notHandlingFlag and not specialMatch:
                review[x] = "not_{}".format(review[x])

            if review[x] == "not":
                notHandlingFlag = True
            
    return data

def openList(filename):
    with open(filename) as f:
        data = json.load(f)

    return data

def clearOutput():

    with open("sentiment-system-answers.txt", "w") as f:
        pass

def classify(decisionList, data):

    clearOutput() # Clear the output file of previous answers

    with open("sentiment-system-answers.txt", "a") as f:
        

        #print(decisionList[0][1]["class"])
        count = 0
        for review in data:
            count += 1
            for x in range(len(decisionList)):
                if(decisionList[x][0] in review):
                    classVal = decisionList[x][1]["class"]
                    output = "{} {}\n".format(review[0], str(classVal))
                    f.write(output)
                    break

def main(fileDecisionList, fileTestData):

    reviewList = preProcess(fileTestData)

    decisionList = openList(fileDecisionList)

    classify(decisionList, reviewList)


def preProcess(filepath):

    result = None

    split = splitData(filepath)
    tokens = tokenData(split)
    notHandlingData = notHandling(tokens)
    result = notHandlingData

    return result

if __name__ == "__main__":

    fileDecisionList = sys.argv[1]
    fileTestData = sys.argv[2]

    main(fileDecisionList, fileTestData)