import json

class Node:

    # Connections (Condition, Direction)
    #   E.g (Finger_Down(5) -> Node(4)[Click])
    def __init__(self):
        """
        
        Args:
            - Value: Int
            - Contections: List[[Int, Int]]
        """
        self.connections = dict()

        self._is_recursive = False

        self.info = {}

    def add_conection(self, to, condition):
        self.connections[condition] = to

    def add_info(self, key, value):
        self.info[key] = value

    def get_info(self, key):
        try:
            result = self.info[key]

            return result
        except:
            return None

    def __contains__(self, objective_node):
        return objective_node in self.connections
    
    def __getitem__(self, i):
        return self.connections[i]

    @property
    def is_recursive(self):
        return self._is_recursive
    
    @is_recursive.setter
    def is_recursive(self, is_recusive):
        self._is_recursive = is_recusive

class ActionGraph:

    BASE_NODE = 0

    def __init__(self, base_gaph):
        
        self.nodes = []

        self.curr_pos = self.BASE_NODE

        self.read_base_graph(base_gaph)

    def read_base_graph(self, base_graph):

        with open('graphs/' + base_graph + '.json', 'r') as f:
            data = json.load(f)

        for _ in range(int(data["number_of_nodes"])):
            temp_node = Node()
            self.nodes += [temp_node]

        for index in data["recursive_nodes"]:
            self.nodes[int(index)].is_recursive = True
        
        for (origin_node, end_node, condition, info) in data["connections"]:
            self.nodes[origin_node].add_conection(end_node, condition)
            if self.nodes[end_node].is_recursive:
                self.nodes[end_node].add_conection(end_node, condition)

        for (node, key, value) in data["info"]:
            self.nodes[node].add_info(key, value)

    def step(self, action):
        if action in self.nodes[self.curr_pos]:
            self.curr_pos = self.nodes[self.curr_pos][action]
        else:
            self.curr_pos = self.BASE_NODE

        return self.curr_pos

    def is_currently_moveable(self):
        if self.nodes[self.curr_pos].get_info("moveable") is not None:
            return self.nodes[self.curr_pos].get_info("moveable")
        
        return False