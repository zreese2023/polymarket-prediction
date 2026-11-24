from polyFeatures import getMarketFeatures, featureNames, hourseBeforeGame, hourSeconds
from evaluateTree import getAccuracy

# Returns the tree's chance and the market price for one game, a given number of hours before it starts

def predictAtTime(gameTree, gameRecord, hoursBefore):

    shiftRecord = dict(gameRecord)
    shiftRecord["start"] = gameRecord["start"] - (hoursBefore - hourseBeforeGame) * hourSeconds

    featureRow = getMarketFeatures(shiftRecord)

    if featureRow is None:

        return None, None

    return gameTree.predictProbability([featureRow])[0], featureRow[featureNames.index("priceNow")]

# Prints one row of the table

def printPrediction(timeLabel, treeChance, marketPrice):

    treePercent = treeChance * 100
    marketPercent = marketPrice * 100

    print(f"{timeLabel:>10}{treePercent:>7.0f}%{marketPercent:>8.0f}%")

def printReliability(treeChance, testChances, testY):

    sameGames = 0
    sameWins = 0

    for i in range(len(testY)):

        if abs(testChances[i] - treeChance) < 0.0001:

            sameGames += 1
            sameWins += testY[i]

    winPercent = sameWins / sameGames * 100

    print(f"  When the tree said {treeChance * 100:.0f}% in {sameGames} test games, the first team won {winPercent:.0f}% of them")

# Compares how often the tree and the market picked the winner on all the test games

def printAccuracy(testChances, testX, testY):

    marketPrices = testX[:, featureNames.index("priceNow")]

    treeAccuracy = getAccuracy(testY, testChances) * 100
    marketAccuracy = getAccuracy(testY, marketPrices) * 100

    print(f"  Overall: tree picked the winner {treeAccuracy:.1f}% of the time, market {marketAccuracy:.1f}%")

def demoGame(gameTree, allRecords, testRows, testX, testY, hoursList = [48, 24, 12, 3]):

    keptRecords = []

    for i in allRecords:

        if getMarketFeatures(i) is not None:
            keptRecords.append(i)

    game = None
    biggestMove = -1

    for rowNumber in testRows:

        earlyChance, earlyPrice = predictAtTime(gameTree, keptRecords[rowNumber], hoursList[0])
        lateChance, latePrice = predictAtTime(gameTree, keptRecords[rowNumber], hoursList[-1])

        if earlyPrice is not None and abs(latePrice - earlyPrice) > biggestMove:

            biggestMove = abs(latePrice - earlyPrice)
            game = keptRecords[rowNumber]

    if game["outcome"] == 1:
        winner = game["outcomes"][0]

    else:
        winner = game["outcomes"][1]

    print(f"Finished game: {game['question']} ({winner} won)")
    print(f"{'Before':>10}{'Model':>8}{'Market':>9}   (chance {game['outcomes'][0]} wins)")

    for hoursBefore in hoursList:

        treeChance, marketPrice = predictAtTime(gameTree, game, hoursBefore)
        printPrediction(str(hoursBefore) + "h", treeChance, marketPrice)

    testChances = gameTree.predictProbability(testX)

    printReliability(treeChance, testChances, testY)
    printAccuracy(testChances, testX, testY)