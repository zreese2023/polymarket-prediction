# The goal of polyTree is to build a decision tree from scratch that learns from the data obtained in polyFeatures.py

import numpy as np

class Node:

    def __init__(self, winChance, sampleCount):

        self.featureIndex = None
        self.threshold = None
        self.left = None
        self.right = None
        self.winChance = winChance
        self.sampleCount = sampleCount

    def isLeaf(self):

        return self.featureIndex is None

def groupImpurity(groupOutcomes):

    # Need to calculate the gini

    return 0.0
    
class DecisionTree:

    def __init__(self, maxDepth = 5, minSamplesLeaf = 20):

        self.maxDepth = maxDepth
        self.minSamplesLeaf = minSamplesLeaf
        self.root = None

    def fit(self, X, Y):

        X = np.asarray(X, dtype = float)
        Y = np.asarray(Y, dtype = float)

        self.root = self.growTree(X, Y, 0)

        return self

    def growTree(self, X, Y, currentDepth):

        # Need to make a node, stop if it should be a leaf or split and grow left and right

        return None

    def findBestSplit(self, X, Y):

        bestFeature = None
        bestThreshold = None
        bestScore = groupImpurity(Y)

        # Need to try every feature and threshhold, keep the best

        return bestFeature, bestThreshold

    
    def predictProbability(self, X):

        X = np.asarray(X, dtype = float)
        allChances = []

        # Need to loop over ever row in X, walk each row down the trea to a leaf and return the winChance

        return np.array(allChances)