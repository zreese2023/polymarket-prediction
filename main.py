# The goal of polyMain is to run everything in order

import numpy as np

from Polydata import getSportsTags, getClosedMarketData
from polyClean import cleanMarkets
from polyFeatures import buildDataset
from polyTree import DecisionTree
from evaluateTree import timeSplit, compareResults

wantedSports = ("nba", "nfl")

def main():

    allRecords = []
    seenIds = set()

    # Download and clean the markets for each sport

    # Turn each market into a row of numbers

    # Train older games, test on newer games

    # Train the tree

    # Compare tree against a market and 50/50 coinflips

    pass

if __name__ == "__main__":
    main()