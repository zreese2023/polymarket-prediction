# The goal of polyFeatures is to turn each cleaned market from polyClean.py into one row of numbers the tree can learn from

# Every feature can only use prices from before the prediction time, this is to avoid lookahead bias

import math
import numpy as np

hourseBeforeGame = 3
hourSeconds = 3600

sportsList = ["nba", "nfl"]

featureNames = [
    "priceNow",          # first team's price at prediction time, this is also the market's own guess (our baseline)
    "price3hAgo",
    "price6hAgo",
    "price12hAgo",
    "price24hAgo",
    "change6h",          # priceNow - price6hAgo
    "change24h",         # priceNow - price24hAgo
    "volatility24h",     # how jumpy the price was over the last 24 hours
    "logVolume",         # log of dollars traded, so huge markets don't drown out everything else
    "hoursListed",       # how long the market had been open at prediction time
]

#Helpers

#Finds the last known price at or before time t

def priceAt(times, prices, t):

    low = 0
    high = len(times) - 1
    answer = 0

    while low <= high:

        middle = (low + high) // 2

        if times[middle] <= t:
            answer = middle
            low = middle + 1

        else:
            high = middle - 1

    return prices[answer]

# Returns all prices between startTime and endTime

def pricesBetweenStartEnd(times, prices, startTime, endTime):

    betweenPrices = []

    for i in range(len(times)):

        if startTime <= times[i] <= endTime:

            betweenPrices.append(prices[i])

    return betweenPrices

#Features

# Returns a list of numbers in the same order as featureNames, or None if there is no price history before prediction time

def getMarketFeatures(marketRecord):

    marketTimes = marketRecord["times"]
    marketPriceList = marketRecord["prices"]
    predictionTime = marketRecord["start"] - hourseBeforeGame * hourSeconds

    # Need to return None if marketTimes is empty or marketTimes[0] is after predictionTime

    # Need to get priceNow with priceAt(marketTimes, marketPriceList, predictionTime)

    # Need to get the older prices the same way, for example price6hAgo = priceAt(marketTimes, marketPriceList, predictionTime - 6 * hourSeconds)

    # Need to get the changes, for example change6h = priceNow - price6hAgo

    # Need to get volatility24h: take pricesBetweenStartEnd(marketTimes, marketPriceList, predictionTime - 24 * hourSeconds, predictionTime), find the difference between each price and the next one, then use np.std on the differences

    # Need to get logVolume with math.log1p(marketRecord["volume"])

    # Need to get hoursListed with (predictionTime - marketTimes[0]) / hourSeconds

    # Need to return numbers as a list

    return None

# Returns X (One row of numbers per market), Y (1 or 0 for who won), game start times, and market prices

def buildDataset(cleanRecords):

    allRows = []
    allOutcomes = []
    allStartTimes = []

    for i in cleanRecords:

        featureRow = getMarketFeatures(i)

        if featureRow is None:
            continue

        allRows.append(featureRow)
        allOutcomes.append(i["outcome"])
        allStartTimes.append(i["start"])

    X = np.array(allRows, dtype = float)
    Y = np.array(allOutcomes, dtype = int)

    startTimes = np.array(allStartTimes)

    if len(X) == 0:
        print ("No markets had enough price history before the game")

        return X, Y, startTimes, np.array([])

    marketPrices =X[:, featureNames.index("priceNow")]

    #Debug for testing
    print(f"Built dataset: {X.shape[0]} games x {X.shape[1]} features")
    return X, Y, startTimes, marketPrices