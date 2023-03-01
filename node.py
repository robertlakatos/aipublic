class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return "<Node {}>".format(self.state)

    def __lt__(self, node):
        return self.state < node.state

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        next_node = Node(state = next_state, 
                         parent = self, 
                         action = action, 
                         path_cost = problem.path_cost(self.path_cost, self.state, action, next_state))
        return next_node

    def expand(self, problem):
        return [self.child_node(problem, action) for action in problem.actions(self.state)]

    def solution(self):
        return [node.action for node in self.path()[1:]]

    def path(self):
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))