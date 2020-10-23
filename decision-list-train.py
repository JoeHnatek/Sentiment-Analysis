"""
Written by: Joseph Hnatek
Date: Oct. 23, 2020

== OVERALL ==
This program will train sentiment analysis by creating a decision list.
This program will then output the decision list to sentiment-decision-list.txt 

== EXAMPLE ==
python3 decision-list-train.py data/sentiment-train.txt

> OUPUT FILE <
seagal 0 5.9581121091291385
chicken--run 1 4.919172024394057
"--chicken 1 4.919172024394057
bateman 1 4.919172024394057
gladiator 1 4.874777905035604
maximus 1 4.828974215422479


== ALGORITHM ==
Read the training file from the user.
Process the data first by spliting the reviews into seperate lists by the newline char.
Tokenize the reviews so we can get unigrams.
Apply the not_handling to the unigrams.
Generate the bigrams of the review text, then add it to the review text.
Seperate the reviews into their respective class within a dictionary.
Create the positive and negative ngram count for positive and negative classified words within the reviews.
Classify whether a word is positive or negative depending on whether the word appears more in positive or negative reviews.
Generate the decision list and sort it based on the hightest to lowers log computation.
Write the decision list to sentiment-decision-list.txt.
"""

import re
import sys
import math
import random
import json
from pprint import pprint
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
        del r[0]    # Remove the filename, we do not need it.

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

def bundleData(data):
    """
    bundleData will create a single dictionary that contains a positive and negative dictionay
    """

    reviews = {"pos": [], "neg": []} # Gross dictionary to 'bundle' our data.

    for token in data: # If the token is in the negative review, add it to the negative dictionary.
        if(token[0]) == '0':
            del token[0]
            reviews["neg"].append(token)
        else:           # If the token is in the positive review, add it to the positive dictionary.
            del token[0]
            reviews["pos"].append(token)

    return reviews
            
def getNgramCounts(data):
    """
    getNgramCounts will insert a token in their respective class and will gather a count of that token so we can
    calculate the probability
    """

    ngramCount = {"pos": {}, "neg": {}} # Another gross dictionary that holds the counts of each word within a class.

    for key, review in data.items():
        for tokens in review:
            for token in tokens:
                if token not in ngramCount[key]:    # If the token is not in the dictionary, add it.
                    ngramCount[key][token] = 1
                else:
                    ngramCount[key][token] += 1 # Add one to the value of token if it is already in there.

    return ngramCount

def classify(wordList, ngrams):
    """
    Classify will assign the unigram or bigram to their respected class.
    If 'the' appears more in positive than negative, then assign it to be positive.
    If 'the' appears more in negative than positive, then assign it to be negative.
    If 'the' does not appear more in positive or negative, then flip a coin.
    """

    positive = ngrams['pos']
    negative = ngrams['neg']

    result = {}

    for word in wordList:

        if word not in positive:    # If word not in positive, assign it negative
            result[word] = 0
            continue

        if word not in negative:    # If word not in negative, assign it positive
            result[word] = 1
            continue
        
        if(positive[word] > negative[word]):    # If word appears more in positive than negative, assign it to positive.
            result[word] = 1
        elif (positive[word] < negative[word]): # If word appears more in negative than positive, assign it to negative.
            result[word] = 0
        else:
            result[word] = random.randint(0, 1) # Flip a coin to decide what it should be assigned to.
    
    return result

def countLength(id, ngrams):
    """
    CountLength will return the total of words within all positive or negative reviews
    """

    count = 0

    for word, value in ngrams[id].items():
        count += value

    return count

def clearOutput():
    """
    Clear the output file from previous training.
    """
    with open("sentiment-decision-list.txt", "w") as f:
        pass

def createDecisionList(ngrams, review, posVocabLength, negVocabLength, reviewVocabLength, masterClassified):
    """
    CreateDecisionList does that. It will calcualte the absolute log function of the positive and negative probability.

    abs(log2(P(good | positive) / P(good | negative)))

    """

    positive = ngrams['pos']
    negative = ngrams['neg']

    discussionList = {}

    for word in review:
        
        if word in positive:
            x = ngrams["pos"][word] + 1 # If the word appears in the positive dictionary, then get the count and add 1
        else: 
            x = 1   # If the word does not exist in the positive dictionary, then 0 + 1

        if word in negative:
            y = ngrams["neg"][word] + 1 # If the word appears in the negative dictionary, then get the count and add 1
        else:
            y = 1    # If the word does not exist in the negative dictionary, then 0 + 1

        # reviewVocabLength is the |V| of unique words for smoothing

        p = (x / (posVocabLength + abs(reviewVocabLength))) # P(good | positive)
        p1 = (y / (negVocabLength + abs(reviewVocabLength)))    # P(good | negative)
        
        value = abs(math.log2(p/p1))

        discussionList[word] = {"val": value, "class": masterClassified[word]}  # Create and return the discussion list

    return discussionList

def writeListToFile(discussionList):
    """
    WriteListToFile will output the discussion list to the sentiment-decision-list.txt as JSON data.
    """
    clearOutput()

    sortedDiscussionList = sorted(discussionList.items(), key=lambda x: x[1]["val"], reverse=True)  # We must sort the discussion list based on the Log value we computed

    with open("sentiment-decision-list.txt", "w") as filename:
        #json.dump(sortedDiscussionList, filename, indent=4) # Write the list in JSON for easy viewing
        for i in range(len(sortedDiscussionList)):
            filename.write("{} {} {}\n".format(sortedDiscussionList[i][0], sortedDiscussionList[i][1]["class"], sortedDiscussionList[i][1]["val"]))


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

            newTokens.append('--'.join(review[i : i + 2]))   # Generate the bigrams of the review text
        
        review.extend(newTokens)    # Add the new bigrams to the original review for easy computation
        newTokens = []
        
    return reviewsList
    
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
        
def main(filepath):

    processedData = preProcess(filepath)    # Preprocess the data

    classifiedData = bundleData(processedData)  # Classify the data
    ngrams = getNgramCounts(classifiedData) # Create the positive and negative ngrams

    posVocab = list(ngrams['pos'].keys())   # Get the unique words in positive words
    negVocab = list(ngrams['neg'].keys())   # Get the uniqie words in negative words
    reviewVocab = list(set(posVocab).union(negVocab))   # Get the total corpus of unique words

    posVocabLength = countLength("pos", ngrams) # Get the total number of positive vocab
    negVocabLength = countLength("neg", ngrams) # Get the total number of negative vocab

    reviewVocabLength = len(reviewVocab)    # Get the length of unique words

    masterClassified = classify(reviewVocab, ngrams)    # Classify a word to be positive or negative depending on how many times it occurs in a review

    disList = createDecisionList(ngrams, reviewVocab, posVocabLength, negVocabLength, reviewVocabLength, masterClassified)    # Create the decisionList

    writeListToFile(disList)    # Write the decision list to the file as JSON data


if __name__ == "__main__":

    filepath = sys.argv[1]  # Grab the filename of the training data

    main(filepath)  # Run the program
