import itertools

actions = [True, False]
discountFactor = 0.9
numFeatStateCom, numFeatStateSim = 7, 4
# allStates = cartesianProduct(actions)
allStates = ((True, True, True, True), (True, True, True, False), (True, True, False, True), (True, True, False, False), (True, False, True, True), (True, False, True, False), (True, False, False, True), (True, False, False, False), (False, True, True, True), (False, True, True, False), (False, True, False, True), (False, True, False, False), (False, False, True, True), (False, False, True, False), (False, False, False, True), (False, False, False, False))
stateTransitionDistances, stateTransitionProbabilities = {}, {}
thresholdRelevance = 2/3
thresholdReward = 0.1

class State:
    def __init__(self, features = (0,)*numFeatStateCom):
        
        self.featCom = features
        self.Npp, self.Nsp, self.Nss, self.Rprev, self.Rsame, self.Rurl = self.featCom
        self.otherStates = None

        # Refer to Section 4.2
        # Simplified Feature #1
        # Host Parse-Skip Ratio
        self.Rspb = True \
            if self.Nsp == 0 or \
                (Nss > 0 and self.Nsp/self.Nss < 1) \
            else False
        # Simplified Feature #2
        # Mean Average Relevance (Previous Host)
        self.Ravgdb = True \
            if self.Rprev == 0 or \
                (self.Tprev > 0 and self.Rprev/self.Tprev >= thresholdRelevance) \
            else False
        # Simplified Feature #3
        # Mean Average Relevance (Current Host)
        self.Ravgsb = True \
            if self.Rsame == 0 or \
                (self.Tsame > 0 and self.Rsame/self.Tsame >= thresholdRelevance) \
            else False
        # Simplified Feature #4
        # Predicted Relevance via URL
        self.Rurlb = True \
            if self.Rurl >= thresholdRelevance \
            else False
        
        self.featSim = (self.Rspb, self.Ravgdb, self.Ravgsb, self.Rurlb)

    # Returns a tuple of complex features
    def getFeatures():
        return self.featCom

    # Returns a tuple of simplified features
    def getState():
        return self.featSim

    # Checks the dictionary for the probabilities
    # Returns the corresponding value if present else calculate new
    def getNextState():
        updateProbabilities(self, actions, self.getOtherStates())
        return stateTransitionProbabilities[self.getState()]

    # Returns a list of other states
    def getOtherStates():
        if self.otherStates == None:
            return allStates.remove(self.getState())
        else:
            return self.otherStates

def updateDistances(state):
    for other in state.getOtherStates():
        d = distance(state, other)
        v = (state, other)
        if d not in stateTransitionDistances:
            stateTransitionDistances[d] = v
        else:
            stateTransitionDistances[d].append(v)

# Returns the distance/probability between 2 states
def distance(s1, s2):
    pass

def updateProbabilities(state):
    if state.getState() not in stateTransitionProbabilities:
        updateDistances(state)

# Reward function
# Normalised number of simplified features labelled True
def reward(state):
    if isinstance(state, State):
        stateIterable = state.getState()
    else:
        stateIterable = state
    return len([f for f in stateIterable if f]) # / numFeatStateSim

# Value function
def value(state):
    currentReward = reward(state)
    if currentReward < rewardThreshold:
        nextReward = 0
    else:
        nextReward = discountFactor * value(state.getNextState())
    return currentReward + nextReward

# Returns combinations with replacement + permutations
def cartesianProduct(options):
    return itertools.product(options, repeat = numFeatStateSim)

def generateTransitionRewardMap(stateTuple, rewardFunction):
    transitionRewardMap = []
    for s1 in stateTuple:
        for s2 in stateTuple:
            for action in actions:
                tempMap = {'state_transitions': [], 'reward': -1}
                tempMap['state_transitions'].append( \
                    { 'state': str(s1), 'action': action, 'state_': str(s2) })
                rewardS1, rewardS2 = rewardFunction(s1), rewardFunction(s2)
                if action:
                    if rewardS2 >= rewardS1:
                        tempMap['reward'] = rewardS2
                    else:
                        tempMap['reward'] = rewardS1
                else:
                    if rewardS2 >= rewardS1:
                        tempMap['reward'] = -1
                    else:
                        tempMap['reward'] = rewardS1
                transitionRewardMap.append(tempMap)
    return transitionRewardMap

# TEST
def test():
    transitionRewardMap = generateTransitionRewardMap(allStates, reward)
    with open('mapping.py', 'w') as f:
        f.write('transitionRewardMap = %s' % str(transitionRewardMap))
    f.close()
    # print(list(map(lambda x: x['reward'], transitionRewardMap)))

# test()
