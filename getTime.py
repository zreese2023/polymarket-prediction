# Looks at the prices at specific hours of a game and determines when is the best time to buy assuming you don't sell, and the best time to sell, assuming you want to sell

from polyFeatures import priceAt, hourSeconds

hoursList = [48, 36, 24, 12, 6, 3]

def getGamePrices(allRecords, gameHours):

    gamesArr = []

    for i in allRecords:

        if len(i["times"]) > 0 and i["times"][0] <= i["start"] - gameHours * hourSeconds:
            gamesArr.append(i)

    return gamesArr

# Gets the best time to buy, using the market's favorite at each hour until the game ends

def showBestBuy(allRecords, hoursList):

    gamesPrices = getGamePrices(allRecords, max(hoursList))

    if len(gamesPrices) == 0:
        print("No games with prices that early")
        return

    print(f"\nBest time to buy and hold the market's favorite ")
    print(f"{'Buy at':>8}{'Avg price':>11}{'Won':>8}{'Profit per share':>18}")

    for i in hoursList:

        totalPrice = 0
        totalWins = 0

        for j in gamesPrices:

            firstTeamPrice = priceAt(j["times"], j["prices"], j["start"] - i * hourSeconds)

            if firstTeamPrice >= 0.5:

                totalPrice += firstTeamPrice
                totalWins += j["outcome"]

            else:

                totalPrice += 1 - firstTeamPrice
                totalWins += 1 - j["outcome"]

        averagePrice = totalPrice / len(gamesPrices)
        winRate = totalWins / len(gamesPrices)
        potentialProfit = winRate - averagePrice

        print(f"{str(i) + 'h':>8}{averagePrice * 100:>10.1f}c{winRate * 100:>7.1f}%{potentialProfit * 100:>16.1f}c")

# Best time to sell: buy the favorite at the earliest time, then sell before the game at each later time

def showBestSell(allRecords, hoursList):

    buyHours = max(hoursList)
    gamesPrices = getGamePrices(allRecords, buyHours)

    if len(gamesPrices) == 0:
        print("No games with prices that early")
        return

    print(f"\nBest time to sell after buying the favorite")
    print(f"{'Sell at':>8}{'Avg change':>12}{'Big swings':>12}")

    for hoursBefore in hoursList:

        if hoursBefore == buyHours:
            continue

        totalChange = 0
        bigSwings = 0

        for i in gamesPrices:

            buyPrice = priceAt(i["times"], i["prices"], i["start"] - buyHours * hourSeconds)
            sellPrice = priceAt(i["times"], i["prices"], i["start"] - hoursBefore * hourSeconds)

            if buyPrice >= 0.5:

                priceChange = sellPrice - buyPrice

            else:
                
                priceChange = (1 - sellPrice) - (1 - buyPrice)

            totalChange += priceChange

            if abs(priceChange) > 0.05:
                bigSwings += 1

        averageChange = totalChange / len(gamesPrices)
        swingRate = bigSwings / len(gamesPrices)

        print(f"{str(hoursBefore) + 'h':>8}{averageChange * 100:>11.1f}c{swingRate * 100:>11.0f}%")