# The goal of data.py is to download and save the Polymarket sports market data so it can be cleaned and used for the tree

# Sports list:    https://docs.polymarket.com/api-reference/sports/get-sports-metadata-information.md
# Market list:    https://docs.polymarket.com/market-data/discover-markets.md
# Price history:  https://docs.polymarket.com/market-data/prices-order-books.md

# Pagination data and id references came from https://docs.polymarket.com/api-reference/markets/list-markets-keyset-pagination.md

import json
import os
import time
import requests

gammaDate = "https://gamma-api.polymarket.com"
polyAPI = "https://data-api.polymarket.com"
cacheDir = "cache"

# Helper functions

def getJson(url, params=None, retries=4):

    for i in range(retries):

        webResponse = requests.get(url, params=params, timeout=20)

        if webResponse.status_code == 429:
            time.sleep(2 ** i)
            continue

        webResponse.raise_for_status()
        return webResponse.json()

    raise RuntimeError(f"Gave up on {url}")

def saveJson(fileName, Obj):

    os.makedirs(cacheDir, exist_ok=True)
    f = open(os.path.join(cacheDir, fileName), "w")
    json.dump(Obj, f)
    f.close()

def loadJson(fileName):

    path = os.path.join(cacheDir, fileName)

    if not os.path.exists(path):
        return None

    f = open(path)
    webData = json.load(f)
    f.close()

    return webData

#Downloading the polymarket data

# Returns the lists of sports names for the sports markets we want to single out, this can be changed

def getSportsTags(wantedSports =("nba", "nfl")):

    sportsData = getJson(f"{gammaDate}/sports")
    sportsTags = {}

    for i in sportsData:

        if i["sport"] not in wantedSports:
            continue

        sportsTags[i["sport"]] = [i["primaryTagId"]]

    return sportsTags

# Collect closed markets for one tag, this is used to get the data for the tree

def getClosedMarketData(tag_id, maxMarkets = 2000):

    cachedData = loadJson(f"markets_{tag_id}.json")

    if cachedData is not None:
        return cachedData

    markets = []
    cursor = None

    while len(markets) < maxMarkets:

        polymarketParameters = {"tag_id": tag_id, "closed": "true", "limit": 100, "sports_market_types": "moneyline"}
        if cursor:
            polymarketParameters["after_cursor"] = cursor

        polyPage = getJson(f"{gammaDate}/markets/keyset", polymarketParameters)

        markets += polyPage.get("markets", [])

        print(f"Tag {tag_id}: downloaded {len(markets)} markets")

        cursor = polyPage.get("next_cursor")

        if not cursor:
            break

        time.sleep(0.2)

    saveJson(f"markets_{tag_id}.json", markets)
    return markets

# Price history for one outcome, bucketSeconds are for how far apart price points are in the markets history, 10800 is 3 hours, we can change this

def getPriceHistory(tokenId, bucketSeconds = 10800):

    cursor = None
    allPoints = []
    name = f"history_{tokenId[:24]}.json"
    cacheData = loadJson(name)

    if cacheData is not None:

        return cacheData

    while True:

        priceHistoryData = {

            "token_id": tokenId,
            "interval": "max",
            "bucket_seconds": bucketSeconds,
        }

        if cursor:
            priceHistoryData["cursor"] = cursor

        priceHistoryData = getJson(f"{polyAPI}/v2/prices-history", priceHistoryData)

        allPoints += priceHistoryData.get("data", [])

        pageInfo = priceHistoryData.get("pagination") or {}
        cursor = pageInfo.get("next_cursor")

        if not pageInfo.get("has_more") or not cursor:
            break

    priceHistory = []

    for i in allPoints:

        if i.get("resolution_seconds") == 0:
            continue

        priceHistory.append({"t": int(i["timestamp"]), "p": float(i["price"])})

    priceHistory.sort(key=lambda point: point["t"])
    
    saveJson(name, priceHistory)
    
    time.sleep(0.1)
    return priceHistory