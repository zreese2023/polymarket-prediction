# The goal of evaluteTree is to measure how good the predictions are, comparing the tree against the market

import numpy as np

def timeSplit(X, Y, startTimes, testFraction = 0.2):

    oldestToNewest = np.argsort(startTimes)

    timeCutoff = int (len(oldestToNewest) * (1 - testFraction))

    trainRows = oldestToNewest[:timeCutoff]
    testRows = oldestToNewest[timeCutoff:]

    return X[trainRows], X[testRows], Y[trainRows], Y[testRows], testRows

def getAccuracy(testY, winChances):

    # Need to count how many games were predicted right and divide by the number of games

    return 0.0

def getBrierScore(testY, winChances):

    # Need to calculate the brier score

    return 0.0

# Grooups predictions into bins

def getCalibration(testY, winChances, binCount = 10):

    # Need to return a list of (average predicted chance, actual win rate, number of games) for each bin that has games

    return []

# Prints a tablet comparing every predictor on the same test games

def compareResults(testY, allPredictions):

    print(f"{'Model':<16}{'Accuracy':>10}{'Brier':>10}")

    for i in allPredictions:

        winChances = allPredictions[i]

        print(f"{i:<16}{getAccuracy(testY, winChances):>10.3f}{getBrierScore(testY, winChances):>10.4f}")