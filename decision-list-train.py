import re
import sys

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



if __name__ == "__main__":

    filepath = sys.argv[1]

    splitData = splitData(filepath)
    tokens = tokenData(splitData)
    notHandlingData = notHandling(tokens)