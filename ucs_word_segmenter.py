import uniform_cost_searcher as util

class WordSegmentationProblem(util.SearchProblem):
    def __init__(self, labels, costDict, maxSyllableLength):
        self.labels = labels
        self.costDict = costDict
        self.maxSyllableLength = maxSyllableLength

    #state is (string: word left, int - index of word we're looking on)
    def startState(self):
        return (self.labels, 0)

    def isEnd(self, state):
        return state[0] == () #when leftover is empty tuple

    def succAndCost(self, state):
        result = []
        # looks at possible 'word step' that we must take
        for i in range(self.maxSyllableLength):
            if(i < len(state[0])):
                subSeg = tuple(state[0][0:i+1])
                nextState = state[0][i+1:]
                thisActionCost = self.costDict[subSeg]
                result.append((subSeg, (nextState, state[1]+1), thisActionCost))

        return result

def segmentWord(labels, costDict, maxSyllableLength):

    ucs = util.UniformCostSearch(verbose=0)
    ucs.solve(WordSegmentationProblem(labels, costDict, maxSyllableLength))
    print("Right actions are ", ucs.actions)
    return ucs.actions
