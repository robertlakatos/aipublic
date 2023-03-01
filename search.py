import numpy as np
from libs.node import Node

def trial_error(problem):
    state = Node(problem.initial)

    while True:
        if problem.goal_test(state.state):
            return state
 
        succesors=state.expand(problem)
        if len(succesors)==0:
            return 'Unsolvable'

        state=succesors[np.random.randint(0,len(succesors))]
        print(state)

def hill_climbing_for_3Cup(problem, heuristic):
    state = Node(problem.initial)

    while True:
        if problem.goal_test(state.state):
            return state

        succesors=state.expand(problem)

        test_succesors=[]
        for s_test in succesors:
            if heuristic(state.state)>=heuristic(s_test.state):
                test_succesors.append(s_test)

        if len(test_succesors)==0:
            return 'Unsolvable'

        state=test_succesors[np.random.randint(0,len(test_succesors))]