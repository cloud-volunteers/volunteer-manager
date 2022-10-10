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
        dict_x[str(i)] = str(x)
    reverse_dict_x = {y: x for x, y in dict_x.items()}
    dict_y = {}
    for i,y in enumerate(y_list):
        dict_y[str(len(x_list)+i)] = str(y)
    reverse_dict_y = {y: x for x, y in dict_y.items()}
    nodes = [Node() for i in range(number)]
    for x,y in nodes_list:
        nodes[int(reverse_dict_x.get(str(x)))].neighbors.append(nodes[int(reverse_dict_y.get(str(y)))])
    match = Match(nodes)
    match.maximum_matching()
    matches = []
    for node in match.nodes:
        if node.mate is not None:
            matches.append((node, node.mate))
    matches_filtered = [tuple(x) for x in set(map(frozenset, matches))]
    output = []
    common_dict = dict_x | dict_y
    for x,y in matches_filtered:
        output.append((int(common_dict.get(str(int(str(x))-int(str(match.nodes[0]))))), int(common_dict.get(str(int(str(y))-int(str(match.nodes[0])))))))

    return output