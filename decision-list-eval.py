"""
Written by: Joseph Hnatek
Date: Oct. 23, 2020

== OVERALL ==
This program evaulates whether or not our training and testing program was successful enough to classify reviews as positive or negative.
== EXAMPLE ==
python3 decision-list-eval.py data/sentiment-gold.txt sentiment-system-answers.txt

...
cv445_tok-23877.txt 1 | cv445_tok-23877.txt 0 | False
cv076_tok-14419.txt 0 | cv076_tok-14419.txt 0 | True
cv368_tok-7890.txt 1 | cv368_tok-7890.txt 0 | False
cv192_tok-29416.txt 0 | cv192_tok-29416.txt 0 | True
cv338_tok-20112.txt 1 | cv338_tok-20112.txt 1 | True
cv065_tok-11153.txt 0 | cv065_tok-11153.txt 0 | True
cv279_tok-15969.txt 1 | cv279_tok-15969.txt 1 | True
cv022_tok-25633.txt 0 | cv022_tok-25633.txt 0 | True
cv426_tok-12735.txt 1 | cv426_tok-12735.txt 0 | False
cv031_tok-25886.txt 0 | cv031_tok-25886.txt 1 | False
Precision: 0.7093023255813954
Recall: 0.61
Accuracy: 0.68

== ALGORITHM ==
Process the actual answers and system answers into their own lists and then tokenize them for easy comparison.
Evaluate whether the system was able to answer correctly compared to the gold standard.
If actual and test are the same classification:
    If actual and test is positive:
        then its True Positive
    else actual and test is negative:
        then its True Negative
else if actual and test are not the same classification:
    If actual is 0 and test is 1
        then its False Positive
    else actual is 1 and test is 0
        then its False Negative
Calculate precision, recall, and accuracy.
Output the results to the sentiment-system-answers-scored.txt file.
"""
import sys

def splitData(filepath):
    """
    Split data with seperate the reviews into their own lists
    """

    with open(filepath) as file:    # Open the reviews text file.
        data = file.read()

    data = data.split('\n') # Split the code on a new line, so each review is its own list.

    del data[-1]    # Remove the very last new line [..., ' '].

    return data
def tokenData(data):
    """
    tokenData will tokenize each review into unigrams
    """

    tokenList = []

    for review in data: # For each review, tokenize the review into unigrams.
        r = review.split()

        tokenList.append(r)
    
    return tokenList

def evaluate(actualAnswers, testAnswers):
    """
    Evaluate if the review is positive or negative.
    """
    clearOutput()

    truePositive = 0
    trueNegative = 0

    falsePositive = 0
    falseNegative = 0

    for x in range(len(actualAnswers)): # Iterate 0 to the number of gold standard answers.

        filenameActual = actualAnswers[x][0]    # Set the gold standard filename
        classificationActual = int(actualAnswers[x][1]) # Set the gold standard classification

        filenameTest = testAnswers[x][0]    # Set the system answers filename
        classificationTest = int(testAnswers[x][1]) # Set the system answers classification

        if((classificationActual == classificationTest)):   # If the classifications match [ 0==0 or 1==1]
            print("{} {} | {} {} | {}\n".format(filenameActual, classificationActual, filenameTest, classificationTest, classificationActual == classificationTest))
            if(classificationActual == 1):  # If they are both 1, then its True Positive.
                truePositive += 1
            else:
                trueNegative += 1   # If they are both 0, then its True Negative
        elif((classificationActual != classificationTest)): # If the classification is not the same.
            print("{} {} | {} {} | {}\n".format(filenameActual, classificationActual, filenameTest, classificationTest, classificationActual == classificationTest))
            if(classificationActual == 0):  # If the gold standard is 0, then system answer must be 1, so its False Positive
                falsePositive += 1
            else:
                falseNegative += 1  # If the gold standard is 1, then system answer is 0, so its False Negative

        outPutScores(filenameActual, classificationActual, filenameTest, classificationTest)

    precision = (truePositive) / (truePositive + falsePositive) # Calculate precision
    recall = (truePositive) / (truePositive + falseNegative)    # Calculate recall
    accuracy = (truePositive + trueNegative) / (truePositive + falsePositive + trueNegative + falseNegative)    # Calculate accuracy


    print("Precision: {}\nRecall: {}\nAccuracy: {}".format(precision, recall, accuracy)) # Print the output to the console.

    outputStats(precision, recall, accuracy) # Output precision, recall, and accuracy to the file.

def clearOutput():
    """
    Clear the output file from previous training.
    """
    with open("sentiment-system-answers-scored.txt", "w") as f:
        pass

def outPutScores(filenameActual, classificationActual, filenameTest, classificationTest):
    """
    Output the scores of the gold standard and the comparative system answers to a file.
    """

    with open("sentiment-system-answers-scored.txt", "a") as f:
        f.write("{} {} | {} {} | {}\n".format(filenameActual, classificationActual, filenameTest, classificationTest, classificationActual == classificationTest))  # Write to the file.

        
def outputStats(precision, recall, accuracy):
    """
    Output the precision, recall, and accuracy of the system answers compared to the gold standard.
    """

    with open("sentiment-system-answers-scored.txt", "a") as f:
        f.write("Precision: {}\nRecall: {}\nAccuracy: {}".format(precision, recall, accuracy))  # Write to the file.


def main(fileActualAnswers, fileTestAnswers):

    preActualAnswers = splitData(fileActualAnswers) # Split the gold standards into their own lists
    preTestAnswers = splitData(fileTestAnswers) # Split the system answers into the own lists

    actualAnswers = tokenData(preActualAnswers) # Tokenize the gold standards for easy comparison
    testAnswers = tokenData(preTestAnswers) # Tokenize the system answers for easy comparison

    evaluate(actualAnswers, testAnswers)    # Evaluate the gold standard to system answers and write the results to a file


if __name__ == "__main__":

    fileActualAnswers = sys.argv[1] # Get the filename of the gold standard from the user
    fileTestAnswers = sys.argv[2]   # Get the filename of the system answers from the user


    main(fileActualAnswers, fileTestAnswers)    # Run the program