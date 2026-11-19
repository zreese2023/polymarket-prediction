# The goal of polyMain is to run everything in order

import numpy as np

from Polydata import getSportsTags, getClosedMarketData
from polyClean import cleanMarkets
from polyFeatures import buildDataset
from polyTree import DecisionTree
from evaluateTree import timeSplit, compareResults, getCalibration

wantedSports = ("nba", "nfl")

def printCalibration(modelName, testY, winChances):

    print(f"\nCalibration of the {modelName}")
    print(f"{'Avg chance':>12}{'Win rate':>10}{'Games':>8}")

    calibrationRows = getCalibration(testY, winChances)

    for averageChance, actualWinRate, gameCount in calibrationRows:

        print(f"{averageChance:>12.3f}{actualWinRate:>10.3f}{gameCount:>8}")

def main():

    allRecords = []
    seenIds = set()

    sportsTags = getSportsTags(wantedSports)

    for i in sportsTags:

        for j in sportsTags[i]:

            rawMarkets = getClosedMarketData(j)
            allRecords += cleanMarkets(rawMarkets, i, seenIds)

    print(f"{len(allRecords)} clean markets total")

    X, Y, startTimes, marketPrices = buildDataset(allRecords)

    trainX, testX, trainY, testY, testRows = timeSplit(X, Y, startTimes)

    print(f"{len(trainY)} training games, {len(testY)} test games")

    gameTree = DecisionTree(maxDepth = 4, minSamplesLeaf = 50)
    gameTree.fit(trainX, trainY)

    treePredictions = gameTree.predictProbability(testX)
    marketPredictions = marketPrices[testRows]

    print()
    compareResults(testY, {
        "Decision tree": treePredictions,
        "Market price": marketPrices[testRows],
        "Always 50%": np.full(len(testY), 0.5),
    })

    printCalibration("Decision tree", testY, treePredictions)
    printCalibration("Market price", testY, marketPredictions)
    
if __name__ == "__main__":
    main()