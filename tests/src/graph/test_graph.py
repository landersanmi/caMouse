from src.graph.graph import ActionGraph

graph = ActionGraph("base")

print(graph)

print(graph.nodes)
print(graph.nodes[0])
print(graph.nodes[1])

for i in range(len(graph.nodes)):
    print(f"--{i}---")
    print(graph.nodes[i].connections)
    print(graph.nodes[i].is_recursive)
