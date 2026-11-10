# The goal of polyClean is to take the raw polymarket data gather from polydata.py and keep only clean game winner markets the tree can learn off of

import json
from datetime import datetime, timezone
from Polydata import getPriceHistory

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

    # Need to return none if there are not exactly two prices

    # Need to turn the price into floats, winner's price should be 1, loser should be 0

    # Need to return None if neither price is above 0.99, which means the market was voided
    
    return None

# Returns true only for "who wins the game" markets, not spreads, totals, or players 

def isGameWinner(polyMarket):

    marketType = polyMarket.get("sportsMarketType")

    # Need to check which value of sportsMarketType means game winner on a few real market types

    return False

# Returns the time the game started in unix seconds, None if there is missing data

def getGameStart(polyMarket):

    # Still need to use toUnixSeconds on polyMarket.get("gameStartTime"), it can be null, return none if missing

    return None

# Cleaning all the markets for one sport

def cleanMarkets(rawMarkets, currSport, seenIds):

    finalCleanedRecords = []
    droppedCount = 0

    for i in rawMarkets:

        # Need to skip markets whose id is already in seenIds, one market can have several tags, then add the id to seenIds

        # Need to skip markets where isGameWinner is false

        # Need to skip markets where getOutcome or getGameStart is None

        # Need to skip markets with volume under minVolume, use i.get("volumeNum")

        # Meed to get the first token id from parsePolyList(i.get("clobTokenIds"))

        # Need to get the price history with getPriceHistory and skip if it has fewer than the minPricePoints points

        # Need to build the record dictionary from the list and add it to finalCleanedRecords

        pass

    print(f"{currSport}: kept {len(finalCleanedRecords)} of {len(rawMarkets)} markets")

    return finalCleanedRecords