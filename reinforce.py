import mapping
from learn import MarkovAgent

agent = MarkovAgent(mapping.transitionRewardMap)
agent.learn()

policy = agent.policy

print(policy)
print(list(filter(lambda x: x, policy.values())))

'''
policy
{
    '(False, True, True, False)': False,
    '(True, False, False, True)': False,
    '(False, True, True, True)': False,
    '(True, False, True, False)': False,
    '(False, True, False, True)': False,
    '(True, True, True, False)': False,
    '(False, False, True, True)': False,
    '(True, True, True, True)': False,
    '(False, False, False, True)': False,
    '(False, False, False, False)': False,
    '(False, False, True, False)': False,
    '(False, True, False, False)': False,
    '(True, True, False, False)': False,
    '(True, True, False, True)': False,
    '(True, False, True, True)': False,
    '(True, False, False, False)': False
}
'''
