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

def evaluate(actualAnswers, testAnswers):

    truePositive = 0
    trueNegative = 0

    falsePositive = 0
    falseNegative = 0
    

    for x in range(len(actualAnswers)):

        filenameActual = actualAnswers[x][0]
        classificationActual = int(actualAnswers[x][1])

        filenameTest = testAnswers[x][0]
        classificationTest = int(testAnswers[x][1])

        print(filenameActual == filenameTest)

        if((classificationActual == classificationTest)):
            if(classificationActual == 1):
                truePositive += 1
            else:
                trueNegative += 1
        elif((classificationActual != classificationTest)):
            if(classificationActual == 1 and classificationTest == 0):
                falseNegative += 1
            else:
                falsePositive += 1


    precision = (truePositive) / (truePositive + falsePositive)
    recall = (truePositive) / (truePositive + falseNegative)
    accuracy = (truePositive + trueNegative) / (truePositive + falsePositive + trueNegative + falseNegative)

    print("Precision: {}\nRecall: {}\nAccuracy: {}".format(precision, recall, accuracy))

    output(precision, recall, accuracy)

        
def output(precision, recall, accuracy):
    with open("sentiment-system-answers-scored.txt", "w") as f:
        f.write("Precision: {}\nRecall: {}\nAccuracy: {}".format(precision, recall, accuracy))


def main(fileActualAnswers, fileTestAnswers):

    preActualAnswers = splitData(fileActualAnswers)
    preTestAnswers = splitData(fileTestAnswers)

    actualAnswers = tokenData(preActualAnswers)
    testAnswers = tokenData(preTestAnswers)

    evaluate(actualAnswers, testAnswers)






if __name__ == "__main__":

    fileActualAnswers = sys.argv[1]
    fileTestAnswers = sys.argv[2]


    main(fileActualAnswers, fileTestAnswers)