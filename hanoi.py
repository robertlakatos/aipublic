from libs.problem import Problem
from collections import namedtuple
State=namedtuple("State", ["disk","char"])

class Hanoi(Problem):
    def __init__(self, n):
        self.size = n
        super().__init__("1" * n, "3" * n)

    def actions(self, state):
        acts = []
        f1 = state.find("1")
        f2 = state.find("2")
        f3 = state.find("3")
        
        if -1 < f1 and (f1 < f2 or f2 == -1):
            acts.append(State(f1, "2"))

        if -1 < f1 and (f1 < f3 or f3 == -1):
            acts.append(State(f1, "3"))

        if -1 < f2 and (f2 < f1 or f1 == -1):
            acts.append(State(f2, "1"))

        if -1 < f2 and (f2 < f3 or f3 == -1):
            acts.append(State(f2, "3"))

        if -1 < f3 and (f3 < f1 or f1 == -1):
            acts.append(State(f3, "1"))

        if -1 < f3 and (f3 < f2 or f2 == -1):
            acts.append(State(f3, "2"))

        return acts

    def result(self, state, action):
        disk, char = action
        return state[0:disk] + char + state[disk + 1:]