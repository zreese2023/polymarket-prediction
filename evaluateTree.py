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
    
    if winChances is None or testY is None:
        return None
    
    gameNum = len(testY) # expects/assumes list type
    if gameNum < 1:
        return 0

    correctNum = 0
    for i in range(gameNum):

        # prediction is considered correct if greater than 50%
        if winChances[i] >= 0.5 and testY[i] == 1:
            correctNum += 1
        elif winChances[i] < 0.5 and testY[i] == 0:
            correctNum += 1

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

    # bins group games by their predicted chance
    # ex. bin 1 is composed of 0 - 10% non-inclusive
    
    if winChances is None or testY is None:
        return None
    
    bins = []
    calibrationRows = []

    chanceTotals = [0] * binCount
    winTotals = [0] * binCount
    gameCounts = [0] * binCount

    for i in range(binCount):
        ind = float((i+1)/binCount)
        bins.append(ind)
    
    ind = np.digitize(winChances, bins)
    
    
    for i in range(len(winChances)):
        binNum = min(ind[i], binCount - 1)

        # compute (commutative operations only)
        chanceTotals[binNum] += winChances[i]
        winTotals[binNum] += testY[i]
        gameCounts[binNum] += 1
    
    for i in range(binCount):

        if gameCounts[i] == 0:
            continue

        averageChance = float(chanceTotals[i] / gameCounts[i])
        actualWinRate = float(winTotals[i] / gameCounts[i])
        calibrationRows.append((averageChance, actualWinRate, gameCounts[i]))

    return calibrationRows

# Prints a tablet comparing every predictor on the same test games

def compareResults(testY, allPredictions):

    print(f"{'Model':<16}{'Accuracy':>10}{'Brier':>10}")

    for i in allPredictions:

        winChances = allPredictions[i]

        print(f"{i:<16}{getAccuracy(testY, winChances):>10.3f}{getBrierScore(testY, winChances):>10.4f}")