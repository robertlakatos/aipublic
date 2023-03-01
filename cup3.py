from problem import Problem

# Három korsó
class Cup3(Problem):
    def actions(self, state):
        acts = []
        five, three, two = state
        if five > 0 and three < 3:
            acts.append("5-->3")
        if five > 0 and two < 2:
            acts.append("5-->2")
        if three > 0 and five < 5:
            acts.append("3-->5")
        if three > 0 and two < 2:
            acts.append("3-->2")
        if two > 0 and five < 5:
            acts.append("2-->5")
        if two > 0 and three < 3:
            acts.append("2-->3")
        return acts

    def result(self, state, action):
        five, three, two = state
        if action == "5-->3":
            m = min(five, 3-three)
            return (five-m, three+m, two)
        if action == "5-->2":
            m = min(five, 2-two)
            return (five-m, three, two+m)
        if action == "3-->5":
            m = min(three, 5-five)
            return (five+m, three-m, two)
        if action == "3-->2":
            m = min(three, 2-two)
            return (five, three-m, two+m)
        if action == "2-->5":
            m = min(two, 5-five)
            return (five+m, three, two-m)
        if action == "2-->3":
            m = min(two, 3-three)
            return (five, three+m, two-m)