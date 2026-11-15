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

    # Calculate the gini

    if len(groupOutcomes) == 0:
        return 0.0

    winRate = float(np.mean(groupOutcomes))
    return 2.0 * winRate * (1.0 - winRate)
    
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

        node = Node(float(np.mean(Y)), len(Y))

        # stop growing if too pure, too deep, or too few samples
        if currentDepth >= self.maxDepth or len(Y) < 2 * self.minSamplesLeaf or groupImpurity(Y) == 0.0:
            return node

        bestFeature, bestThreshold = self.findBestSplit(X, Y) # find the best feature and threshold to split on

        if bestFeature is None:
            return node

        leftMask = X[:, bestFeature] <= bestThreshold # mask for left branch

        # set the split and grow the branches
        node.featureIndex = bestFeature
        node.threshold = bestThreshold
        node.left = self.growTree(X[leftMask], Y[leftMask], currentDepth + 1)
        node.right = self.growTree(X[~leftMask], Y[~leftMask], currentDepth + 1)

        return node

    def findBestSplit(self, X, Y):

        bestFeature = None
        bestThreshold = None
        bestScore = groupImpurity(Y)

        # Need to try every feature and threshold, keep the best

        count = len(Y)
        wins = float(np.sum(Y))

        for featureIndex in range(X.shape[1]):
            # sort by feature value
            order = np.argsort(X[:, featureIndex], kind="stable")
            values = X[order, featureIndex]
            outcomes = Y[order]

            leftWins = np.cumsum(outcomes) # cumulative wins in left group

            for i in range(self.minSamplesLeaf - 1, count - self.minSamplesLeaf):
                if values[i] == values[i + 1]:
                    continue

                lc = i + 1 # samples in left group
                rc = count - lc # samples in right group
                lr = leftWins[i] / lc # win rate in left group
                rr = (wins - leftWins[i]) / rc # win rate in right group

                leftGini = 2.0 * lr * (1.0 - lr)
                rightGini = 2.0 * rr * (1.0 - rr)

                score = (lc * leftGini + rc * rightGini) / count

                if score < bestScore:
                    bestScore = score
                    bestFeature = featureIndex
                    bestThreshold = (values[i] + values[i + 1]) / 2.0

        return bestFeature, bestThreshold

    
    def predictProbability(self, X):

        X = np.asarray(X, dtype = float)
        allChances = []

        # Need to loop over ever row in X, walk each row down the trea to a leaf and return the winChance
        for row in X:
            node = self.root
            while not node.isLeaf():
                if row[node.featureIndex] <= node.threshold:
                    node = node.left
                else:
                    node = node.right
            allChances.append(node.winChance)

        return np.array(allChances)

    def predict(self, X):
        # convert predicted probabilities to binary class labels
        return (self.predictProbability(X) >= 0.5).astype(int)