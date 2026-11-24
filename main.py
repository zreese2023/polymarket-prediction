# The goal of polyMain is to run everything in order

import numpy as np

from demo import demoGame
from getTime import showBestBuy, showBestSell
from Polydata import getSportsTags, getClosedMarketData
from polyClean import cleanMarkets
from polyFeatures import buildDataset
from polyTree import DecisionTree
from evaluateTree import timeSplit, compareResults

wantedSports = ("nba", "nfl")

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

    print()
    compareResults(testY, {
        "Decision tree": treePredictions,
        "Market price": marketPrices[testRows],
        "Always 50%": np.full(len(testY), 0.5),
    })

    print()
    demoGame(gameTree, allRecords, testRows, testX, testY)

    showBestBuy(allRecords, [48, 36, 24, 12, 6, 3])
    showBestSell(allRecords, [48, 36, 24, 12, 6, 3])
    
if __name__ == "__main__":
    main()