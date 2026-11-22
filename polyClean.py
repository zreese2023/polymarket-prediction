# The goal of polyClean is to take the raw polymarket data gather from polydata.py and keep only clean game winner markets the tree can learn off of

import json
from datetime import datetime, timezone
from Polydata import getPriceHistory
from requests import RequestException

minVolume = 1000
minPricePoints = 4

#Helpers

# Polymarket stores some lists as text, this would turn it into a real list

def parsePolyList(field):

    if isinstance(field, str):

        try:
            return json.loads(field)

        except json.JSONDecodeError:
            return []


    if field is None:
        return []

    return field

# Turns muddy dates into unix seconds, returns none if it is missing

def toUnixSeconds(dateText):

    if not dateText:
        return None

    try:
        return datetime.fromisoformat(dateText.replace("Z", "+00:00")).timestamp()

    except ValueError:
        return None

#Cleaning


# Returns 1 if the first team won, 0 if the second team won, None if result is unclear

def getOutcome(polyMarket):

    getOutcome = parsePolyList(polyMarket.get("outcomePrices"))

    if len(getOutcome) != 2:

        return None

    firstPrice = float(getOutcome[0])
    secondPrice = float(getOutcome[1])

    if firstPrice > 0.99:

        return 1

    if secondPrice > 0.99:

        return 0
    
    return None

# Returns true only for "who wins the game" markets, not spreads, totals, or players 

def isGameWinner(polyMarket):

    marketType = polyMarket.get("sportsMarketType")

    marketOutcomes = parsePolyList(polyMarket.get("outcomes"))

    if marketType != "moneyline":
        return False

    if len(marketOutcomes) != 2 or marketOutcomes == ["Yes", "No"]:
        return False

    return True

# Returns the time the game started in unix seconds, None if there is missing data

def getGameStart(polyMarket):

    gameStart = toUnixSeconds(polyMarket.get("gameStartTime"))

    if gameStart is not None:

        return gameStart

    return toUnixSeconds(polyMarket.get("endDate"))

# Cleaning all the markets for one sport

def cleanMarkets(rawMarkets, currSport, seenIds):

    finalCleanedRecords = []
    droppedCount = 0

    for i in rawMarkets:

        if i.get("id") in seenIds:

            droppedCount += 1
            continue

        seenIds.add(i.get("id"))

        # skip markets where isGameWinner is false

        if not isGameWinner(i):
            droppedCount += 1
            continue

        # skip markets where getOutcome or getGameStart is None

        marketOutcome = getOutcome(i)
        gameStart = getGameStart(i)

        if marketOutcome is None or gameStart is None:
            
            droppedCount += 1
            continue

        # Need to skip markets with volume under minVolume, use i.get("volumeNum")

        volume = i.get("volumeNum")
        if volume is None or volume < minVolume:
            droppedCount += 1
            continue

        # Meed to get the first token id from parsePolyList(i.get("clobTokenIds"))

        tokenIds = parsePolyList(i.get("clobTokenIds"))
        if len(tokenIds) == 0:
            droppedCount += 1
            continue
        tokenId = tokenIds[0]

        # Need to get the price history with getPriceHistory and skip if it has fewer than the minPricePoints points

        try:
            priceHistory = getPriceHistory(tokenId)
        except (RequestException, RuntimeError):
            droppedCount += 1
            continue
        
        if len(priceHistory) < minPricePoints:
            droppedCount += 1
            continue

        # Need to build the record dictionary from the list and add it to finalCleanedRecords

        finalCleanedRecords.append({
            "sport": currSport,
            "id": i.get("id"),
            "start": gameStart,
            "outcome": marketOutcome,
            "volume": float(volume),
            "times": [point["t"] for point in priceHistory],
            "prices": [point["p"] for point in priceHistory],
        })

    print(f"{currSport}: kept {len(finalCleanedRecords)} of {len(rawMarkets)} markets")

    return finalCleanedRecords