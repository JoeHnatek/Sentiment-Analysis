"""
Written by: Joseph Hnatek
Date: Oct. 23, 2020

== OVERALL ==
This program will classify a review as positive or negative based on the decision list generated from the training program.

== EXAMPLE ==
python3 decision-list-test.py sentiment-decision-list.txt data/sentiment-test.txt

> OUTPUT FILE <

cv666_tok-13320.txt 1
cv535_tok-19937.txt 0
cv245_tok-19462.txt 1
cv561_tok-26915.txt 1
cv329_tok-17076.txt 1
cv235_tok-11172.txt 0
cv634_tok-28807.txt 1
cv236_tok-23452.txt 1
cv415_tok-28738.txt 0
cv204_tok-10080.txt 1
...

== ALGORITHM ==
Split the reviews into their own lists for easy processing.
Tokenize the reviews so we have unigrams.
Apply the 'not_handling' to the unigrams.
Generate the bigrams and add it to the review.
Read the decision list from the users input.
For each review, Depending on the words order in the decision list,
If the word is in the review, classify the review as such.
Write the filename and classification to the output file.
"""

import sys
import json
import re
from collections import OrderedDict

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
        del r[1]    # Remove the '__' in the review, we do not need it.

        tokenList.append(r)
    
    return tokenList

def notHandling(data):
    """
    notHandling will append 'not_' to words after not appears in the text
    """

    notHandlingFlag = False

    for review in data:
        for x in range(len(review)):
            
            specialMatch = re.match(r"""[()-,?\/:'"|]""", review[x]) #  Do not append 'not_' to a special char.
            endSentenceMatch = re.match(r'[.!?]', review[x])    # Make sure we can find the end of the sentence.

            if endSentenceMatch and notHandlingFlag:    # Stop appending 'not_' to words.
                notHandlingFlag = False
            elif notHandlingFlag and not specialMatch:  # Append 'not_' to a word.
                review[x] = "not_{}".format(review[x])

            if review[x] == "not":  # If the current word is "not", turn the Flag to True, so we can append 'not_' to the rest of the words.
                notHandlingFlag = True
            
    return data

def bigram(reviewsList):
    """
    Bigram will create the bigrams of the reviews.
    """
    
    step = 1
    N_Gram = 2

    newTokens = []
    
    for review in reviewsList:
        
        for i in range(1, len(review), step):   # Slide across the data based on the step to gather the ngram model.
            # If bigram: ["The red", "red fox", "fox jumped", "jumped ."]

            newTokens.append(' '.join(review[i : i + 2]))   # Generate the bigrams of the review text
        
        review.extend(newTokens)    # Add the new bigrams to the original review for easy computation
        newTokens = []

    return reviewsList

def openList(filename):
    """
    Open the decision list and append it to a list.
    """

    decList = []

    run = True
    count = 0

    data = splitData(filename)  # Split the data by new line for easy comprehension

    for line in data:
        line = line.split() # Split the line by space to seperate the word class and classifier
        line[0] = line[0].replace("--", " ")    # Replace the bigram 'space' between two words
        del line[2] # Remove the log value, we dont need it. List is already in order
        decList.append(line)    # Append the line to the decision list
    
    return decList

def clearOutput():
    """
    Clear the output file from previous training.
    """
    with open("sentiment-system-answers.txt", "w") as f:
        pass

def classify(decisionList, data):
    """
    Based on the decision list, classify will say whether a review is positive or negative.
    """

    clearOutput() # Clear the output file of previous answers

    with open("sentiment-system-answers.txt", "a") as f:

        for review in data: # For each review
            for x in range(len(decisionList)):  # Iterate through the decision list.
                if(decisionList[x][0] in review):   # If the decision list word is in the review, then we found it!
                    classVal = decisionList[x][1]  # Classify whether the review is positive or negative
                    output = "{} {}\n".format(review[0], str(classVal)) # Write to the file with filename {0/1}
                    f.write(output)
                    break   # Stop classifying this review becuase we found a matching word in the decision list

def main(fileDecisionList, fileTestData):

    reviewList = preProcess(fileTestData)   # Preprocess the data

    decisionList = openList(fileDecisionList)   # Get the decision list from the file

    classify(decisionList, reviewList)  # Classify whether a review is positive or negative based on the decision list


def preProcess(filepath):
    """
    preProcess will process the data before we start training the data.
    """
    
    split = splitData(filepath) # Split into their own reviews
    tokens = tokenData(split)   # Tokenize the reviews so we have unigrams
    notHandlingData = notHandling(tokens)   # Do the not handling.

    #bigram module here
    corpus = bigram(notHandlingData)

    return corpus

if __name__ == "__main__":

    fileDecisionList = sys.argv[1]  # Grab the filename of the decision list
    fileTestData = sys.argv[2]  # Grab the test filename

    main(fileDecisionList, fileTestData)    # Run the program
