# The goal of evaluteTree is to measure how good the predictions are, comparing the tree against the market

import numpy as np

def timeSplit(X, Y, startTimes, testFraction = 0.2):

    oldestToNewest = np.argsort(startTimes)

    timeCutoff = int (len(oldestToNewest) * (1 - testFraction))

    trainRows = oldestToNewest[:timeCutoff]
    testRows = oldestToNewest[timeCutoff:]

    return X[trainRows], X[testRows], Y[trainRows], Y[testRows], testRows

# testY: array of actual game outcome 
# winChances: array of predicted chance for each of those games
def getAccuracy(testY, winChances):

    # Count how many games were predicted right and divide by the number of games
    gameNum = len(testY)

    correctNum = 0
    for i in range(gameNum):
        # prediction is considered correct if greater than 50%
        if testY[i] == 1 and winChances[i] > 0.5:
            correctNum += 1 # increment counter of how many game were right

    return float(correctNum/gameNum)

def getBrierScore(testY, winChances):

    # Calculate the brier score

    numInstances = len(testY)

    sum = 0
    for i in range(numInstances):
        addend = float(winChances[i] - testY[i]) ** 2
        sum += addend

    brScore = (1/numInstances) * (sum)

    return brScore

# Groups predictions into bins

def getCalibration(testY, winChances, binCount = 10):

    # Need to return a list of (average predicted chance, actual win rate, number of games) for each bin that has games

    # bins group games by their predicted chance

    return []

# Prints a tablet comparing every predictor on the same test games

def compareResults(testY, allPredictions):

    print(f"{'Model':<16}{'Accuracy':>10}{'Brier':>10}")

    for i in allPredictions:

        winChances = allPredictions[i]

        print(f"{i:<16}{getAccuracy(testY, winChances):>10.3f}{getBrierScore(testY, winChances):>10.4f}")