from algorithm.max_matching import Node, Match

def matching_function(nodes_list):
    x_list = []
    y_list = []
    for x,y in nodes_list:
        x_list.append(x)
        y_list.append(y)
    x_list = list(set(x_list))
    y_list = list(set(y_list))
    number = len(x_list)+len(y_list)
    dict_x = {}
    for i,x in enumerate(x_list):
        dict_x[str(i)] = x
    reverse_dict_x = {y: x for x, y in dict_x.items()}
    dict_y = {}
    for i,y in enumerate(y_list):
        dict_y[str(len(x_list)+i)] = y
    reverse_dict_y = {y: x for x, y in dict_y.items()}
    nodes = [Node() for i in range(number)]
    for x,y in nodes_list:
        nodes[reverse_dict_x.get(x)].neighbors.append(nodes[reverse_dict_y.get(y)])
    match = Match(nodes)
    match.maximum_matching()
    matches = []
    for node in match.nodes:
        if node.mate is not None:
            matches.append((node, node.mate))
    matches_filtered = [tuple(x) for x in set(map(frozenset, matches))]
    output = []
    for x,y in matches_filtered:
        output.append((dict_x.get(x), dict_y.get(y)))
    return output