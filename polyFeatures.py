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
    "change3h",          # priceNow - price3hAgo
    "change6h",          # priceNow - price6hAgo
    "change12h",         # priceNow - price12hAgo
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

    priceDifference = []

    marketTimes = marketRecord["times"]
    marketPriceList = marketRecord["prices"]
    predictionTime = marketRecord["start"] - hourseBeforeGame * hourSeconds

    if len(marketTimes) == 0:
        return None

    if marketTimes[0] > predictionTime:
        return None

    priceNow = priceAt(marketTimes, marketPriceList, predictionTime)

    price3hAgo = priceAt(marketTimes, marketPriceList, predictionTime - 3 * hourSeconds)
    price6hAgo = priceAt(marketTimes, marketPriceList, predictionTime - 6 * hourSeconds)
    price12hAgo = priceAt(marketTimes, marketPriceList, predictionTime - 12 * hourSeconds)
    price24hAgo = priceAt(marketTimes, marketPriceList, predictionTime - 24 * hourSeconds)

    
    change3hour = priceNow - price3hAgo
    change6hour = priceNow - price6hAgo
    change12hour = priceNow - price12hAgo
    change24hour = priceNow - price24hAgo

    lastDayPrice = pricesBetweenStartEnd(marketTimes, marketPriceList, predictionTime - 24 * hourSeconds, predictionTime)

    for i in range(len(lastDayPrice) - 1):

        priceDifference.append(lastDayPrice[i + 1] - lastDayPrice[i])

    if len(priceDifference) < 2:

        volatility24Hours = 0.0

    else:

        volatility24Hours = float(np.std(priceDifference))

    logVolume = math.log1p(marketRecord["volume"])

    hoursListed = (predictionTime - marketTimes[0]) / hourSeconds
    
    return  [priceNow, price3hAgo, price6hAgo, price12hAgo, price24hAgo, change3hour, change6hour, change12hour, change24hour, volatility24Hours, logVolume, hoursListed]


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