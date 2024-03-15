#!/usr/bin/python3
#************************************************************
#   scan_print_map.py
#   Scan a hashi puzzle from stdin, store it in a numpy array,
#   and print it out again.
#
import numpy as np
import sys
nrow = 0
ncol = 0
code = ".123456789abc"
nodes = []
# bridge = {
#     'ends'  : [node_0, node_1],
#     'val'   : int < 0,
#     'is_hor': Bool,
# }
bridges = []
MAX_BRIDGE_NUM = 3

def find_vert(x, y, i_map, nrow):
    hori_neightbours = []
    for i in reversed(range(0, x)):
        if (i_map[i][y] < 0):
            break
        if (i_map[i][y] > 0):
            # print(f"Closest island for {(x,y)} = {i_map[x][y]} in adscending vertical order (top of) is {(i, y)} = {i_map[i][y]}")
            hori_neightbours.append((i, y))
            break
    for i in range(x + 1, nrow):
        if (i_map[i][y] < 0):
            break
        if (i_map[i][y] > 0):
            # print(f"Closest island for {(x,y)} = {i_map[x][y]} in descending vertical order (bottom of) is {(i, y)} = {i_map[i][y]}")
            hori_neightbours.append((i, y))
            break
    return hori_neightbours

def find_hori(x, y, i_map, ncol):
    vert_neightbours = []
    for i in reversed(range(0, y)):
        if (i_map[x][i] < 0):
            # Blocked
            break
        if (i_map[x][i] > 0):
            # print(f"Closest island for {(x,y)} = {i_map[x][y]} in adscending horizontal order (left of) is {(x, i)} = {i_map[x][i]}")
            vert_neightbours.append((x, i))
            break
    for i in range(y + 1, ncol):
        if (i_map[x][i] < 0):
            # Blocked
            break
        if (i_map[x][i] > 0):
            # print(f"Closest island for {(x,y)} = {i_map[x][y]} in descending horizontal order (right of) is {(x, i)} = {i_map[x][i]}")
            vert_neightbours.append((x, i))
            break
    return vert_neightbours

# Given a pair of coordinates representing the an island, find its direct connectable neighbours. 
def find_neighbours(coord, i_map, nrow, ncol):
    x = int(coord[0])
    y = int(coord[1])
    # print(f"Finding for {(x, y)} = {code[i_map[x,y]]}")

    neighbours = find_hori(x, y, i_map, ncol) + find_vert(x, y, i_map, nrow)
    # print(f"All neighbours for {(x, y)} = {code[i_map[x,y]]}: {neighbours}")
    return neighbours

def check_lemma(node):
    # print(f"Checking for\n\t{node}")
    if (node['is_completed']):
        return False
    if (len(node['neighbours']) == 0):
        return False
    # if ()
    return (len(node['neighbours']) == 1 or (node['capacity'] > ((len(node['neighbours']) - 1) * MAX_BRIDGE_NUM)))

def iterative_check(node):
    # Check existing
    return 0

def find_node(node, nodes):
    for idx, n in enumerate(nodes):
        if n['xy'] == node:
            return idx

def bridge_contains(node_0, node_1, bridges):
    for idx, bridge in enumerate(bridges):
        if node_0 in bridge['ends'] and node_1 in bridge['ends']:
            return idx
    return -1
# idx = idx of node_0
def build_bridge(node_0, node_1, idx, i_map, val, nrow, ncol, nodes, bridges):
    # print(f"Trying to build bridge from {node_0} = {i_map[node_0]} to {node_1} = {i_map[node_1]}")
    (x0, y0) = node_0
    (x1, y1) = node_1
    bridge_range = []
    if (x0 == x1):
        horizontal_bridge_range = range(y0 + 1, y1)
        if len(range(y0 + 1, y1)) == 0:
            horizontal_bridge_range = reversed(range(y1 + 1, y0))
        for i in horizontal_bridge_range:
            i_map[x0, i] = val
    elif (y0 == y1):
        vertical_bridge_range = range(x0 + 1, x1)
        if len(range(x0 + 1, x1)) == 0:
            vertical_bridge_range = reversed(range(x1 + 1, x0))
        for i in vertical_bridge_range:
            i_map[i, y0] = val
    else:
        # print(f"Error, bridge cannot be built")
        quit()
    # Update status
    ends = []
    if (x0 <= x1 and y0 <= y1):
        ends = [node_0, node_1]
    else:
        ends = [node_1, node_0]
    bridge_idx = bridge_contains(node_0, node_1, bridges)
    if (bridge_idx != -1):
        bridges[bridge_idx]['val'] += val
    else:
        bridges.append({
            'ends'  : ends,
            'val'   : val,
            'is_hor': x0==x1,
        })
    # print(f"Updating neighbours on the side of ends: {ends}")
    if (x0==x1):
        for i in range(ends[0][1]+1,ends[1][1]):
            # print(f"{(x0, i)}")
            update_neighbours(True, x0, i, i_map, nrow, ncol, nodes)
    else:
        # print(ends[0][0]+1,ends[0][1])
        for i in range(ends[0][0]+1,ends[1][0]):
            # print(f"{(i, y0)}")
            update_neighbours(False, i, y0, i_map, nrow, ncol, nodes)

    idx_1 = find_node(node_1, nodes)
    nodes[idx]['capacity'] += val
    nodes[idx_1]['capacity'] += val

    # print(f"Bridge from {node_0} = {i_map[node_0]} to {node_1} = {i_map[node_1]} built\nAffected nodes:\n\t{nodes[idx]}\n\t{nodes[idx_1]}\nBridge:\n\t{bridges[bridge_idx]}\n============\n")

    if (bridges[bridge_idx]['val'] == -3):
        remove_for_max_bridge(nodes[idx], nodes[idx_1])
    if (nodes[idx]['capacity'] == 0):
        # Current node satisfied. Remove it from others list
        remove_current_node_in_neighbours_storage(nodes[idx])
    if (nodes[idx_1]['capacity'] == 0):
        # Remove it from others list
        remove_current_node_in_neighbours_storage(nodes[idx_1])
    return 0

def update_neighbours(is_hor, x, y, i_map, nrow, ncol, nodes):
    disconnected_islands = []
    if (is_hor):
        disconnected_islands = find_vert(x, y, i_map, nrow)
    else:
        disconnected_islands = find_hori(x, y, i_map, ncol)
    # print(disconnected_islands)
    if len(disconnected_islands) == 2:
        node_0 = disconnected_islands[0]
        node_1 = disconnected_islands[1]
        idx_0 = find_node(node_0, nodes)
        idx_1 = find_node(node_1, nodes)
        node0 = nodes[idx_0]
        node1 = nodes[idx_1]
        info0 = {'node':node_0, 'position':idx_0}
        info1 = {'node':node_1, 'position':idx_1}
        if (info1 in node0['neighbours'] and info0 in node1['neighbours']):
            # Removes
            node0['neighbours'].remove(info1)
            node1['neighbours'].remove(info0)
            # print(f"Removed nodes {node_0} and {node_1} from their neighbours list")
            # print(f"\t{node0}\n\t{node1}")

def remove_for_max_bridge(node_0, node_1):
    node_1['neighbours'].remove(
        {
            'node': node_0['xy'],
            'position': node_0['position']
        }
    )
    node_0['neighbours'].remove(
        {
            'node': node_1['xy'],
            'position': node_1['position']
        }
    )

def remove_current_node_in_neighbours_storage(node):
    # print(f"Removing\n\t{node}\n\tfrom:")
    for neighbour in node['neighbours']:
        # print(nodes[neighbour['position']]['neighbours'])
        nodes[neighbour['position']]['neighbours'].remove({
            'node': node['xy'],
            'position': node['position']
        })
        # print(f"Removed\n\t{node}\nfrom\n\t{nodes[neighbour['position']]}")
    node['neighbours'] = []
    node['is_completed'] = True
        
def code_bridge(is_hor, value):
    bridge_code = "-=E|\"#"
    code_idx = value - 1
    if (not is_hor):
        code_idx += 3
    print(bridge_code[code_idx], end="")

def print_bridge(x, y):
    for bridge in bridges:
        start = bridge['ends'][0]
        end = bridge['ends'][1]
        if (bridge['is_hor']):
            if (x == start[0] and y > start[1] and y < end[1]):
                code_bridge(True, -bridge['val'])
        else:
            if (y == start[1] and x > start[0] and x < end[0]):
                code_bridge(False, -bridge['val'])

def print_map(nrow, ncol, i_map):
    for r in range(nrow):
        for c in range(ncol):
            if (i_map[r,c] >= 0): print(code[i_map[r,c]],end="")
            else: print_bridge(r,c)
        print()

def solve(i_map, node_dict_list, bridge_dict_list, nrow, ncol, i, j, is_test):
    # # Content from last iteration
    # nodes = node_dict_list[-1]['nodes']
    # bridges = bridge_dict_list[-1]['bridges']
    nodes = node_dict_list
    bridges = bridge_dict_list
    # Make own 
    operation = []

    # Base Case: all solved
    fin = True
    for node in nodes:
        if (not node['is_completed']):
            fin = False
    if fin:
        return True

    # If not solved and remaining nodes are finished, Early exit
    ee = True
    for tmp in range(i, len(nodes)):
        if not nodes[tmp]['is_completed']:
            ee = False
    if (ee):
        return False

    if (is_test): print(f"========check {i}th node with its {j}th neighbour========")
    # For Each Node, try BFS
    while i < len(nodes):
        node = nodes[i]
        if (is_test): print(f"Start DFS,\n\tNode: {node}")
        neighbours = node['neighbours']
        # Early exit to next node if current island is finished (neighbour idx == array length)
        if (j >= len(neighbours)):
            if (is_test): print(f"Exceeded node's neighbour")
            i = i + 1
            j = 0
            if solve(i_map, node_dict_list, bridge_dict_list, nrow, ncol, i, j, is_test):
                return True
        # Current neighbour is available, try different options
        else:
            for b in range(0, 4):
                # If a neighbour is finished from iteration, the neighbour is removed from the list, hence minus
                if (len(node['neighbours']) == 0 and node['capacity'] == 0):
                    if (is_test): print(f"Node:\n\t{node} has finished during iteration")
                    if solve(i_map, node_dict_list, bridge_dict_list, nrow, ncol, i + 1, 0, is_test):
                        return True
                    return False
                elif (len(node['neighbours']) == 0 and node['capacity'] > 0):
                    return False
                while (j >= len(neighbours)):
                    j -= 1
                if (is_test): print(f"J = {j}; Node:\n\t{node}")
                neighbour = neighbours[j]
                # Start with no bridge
                if b == 0:
                    if (is_test): print(f"From {node['xy']} to {neighbour['node']} Try no bridge=======================")
                    # Try continue with no bridge
                    if solve(i_map, node_dict_list, bridge_dict_list, nrow, ncol, i, j + 1, is_test):
                        return True
                bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                # Build one bridge from node to neighbour and pass this on to next neighbour / node
                if b == 1:
                    if (is_test): print(f"\n\nNo bridge from {node['xy']} to {neighbour['node']} failed\nFrom {node['xy']} to {neighbour['node']} Try 1 bridge=======================")
                    # Only build one bridge if no bridge has been built
                    if bridge_idx == -1:
                        build_bridge(node['xy'], neighbour['node'], find_node(node['xy'], nodes), i_map, -1, nrow, ncol, nodes, bridges)
                        if (is_test): print_map(nrow, ncol, i_map)
                    else:
                        if (is_test): print("Bridge exists. Skipped")
                    if solve(i_map, node_dict_list, bridge_dict_list, nrow, ncol, i, j + 1, is_test):
                        return True
                if b == 2:
                    if (is_test): print(f"\n\nOne bridge from {node['xy']} to {neighbour['node']} failed\nFrom {node['xy']} to {neighbour['node']} Try 2 bridge=======================")

                    # Only build the second bridge if there is currently exactly one bridge
                    bridge_val = bridges[bridge_idx]['val']
                    if bridge_val == -1:
                        build_bridge(node['xy'], neighbour['node'], find_node(node['xy'], nodes), i_map, -1, nrow, ncol, nodes, bridges)
                        if (is_test): print_map(nrow, ncol, i_map)
                    # else: print("Bridge exists. Skipped")
                    if solve(i_map, node_dict_list, bridge_dict_list, nrow, ncol, i, j + 1, is_test):
                        return True
                if b == 3:
                    if (is_test): print(f"\n\nTwo bridge from {node['xy']} to {neighbour['node']} failed\nFrom {node['xy']} to {neighbour['node']} Try 3 bridge=======================")

                    # Only build the thrid bridge if there is currently exactly two bridges
                    if bridge_val == -2:
                        build_bridge(node['xy'], neighbour['node'], find_node(node['xy'], nodes), i_map, -1, nrow, ncol, nodes, bridges)
                        if (is_test): print_map(nrow, ncol, i_map)
                    else:
                        if (is_test): print("Bridge exists. Skipped")
                    if solve(i_map, node_dict_list, bridge_dict_list, nrow, ncol, i, j + 1, is_test):
                        return True

    if (is_test): print(f"\n==============In solve, checking at {i}th node and {j}th neighbour================")
    
    for node in nodes:
        if (not node['is_completed']):
            return False

    return True

def main():
    nrow, ncol, i_map = scan_map()
    ccc = 0
    # Get islands/nodes
    for r in range(nrow):
        for c in range(ncol):
            if(i_map[r,c] > 0):
                nodes.append({
                    'xy': (r,c),
                    'value':    i_map[r,c],
                    'capacity': i_map[r,c],
                    'neighbours': find_neighbours((r, c), i_map, nrow, ncol),
                    # 'neighbour_of': [],
                    'is_completed': False,
                    'position': len(nodes),
                    # 'bridges': []
                })
                # cur_node = nodes[len(nodes) - 1]
    # For all nodes, give them easier access to their neighbours position
    for node_idx, node in enumerate(nodes):
        new = []
        neighbours = node['neighbours']
        for neighbour in neighbours:
            neighbour_idx = find_node(neighbour, nodes)
            new.append({
                'node': neighbour,
                'position': neighbour_idx,
            })
            # nodes[neighbour_idx]['neighbour_of'].append({
            #     'node': node['xy'],
            #     'position': node_idx,
            # })
        node['neighbours'] = new

    # print(f"Initialisation complete:")
    # for node in nodes:
    #     print(node)
    # For all nodes, try apply the lemma to link islands that must be connected before applying other search strategies
    init_complete = False
    while (not init_complete):
        init_complete = True
        ccc+=1
        # print(f"\n\nIterating\n\n")
        for idx, node in enumerate(nodes):
            # May also want to update check_lemma to iterate using the list of dict
            if check_lemma(node):
                # print(f"Node: {node['xy']} satisfies lemma. Building bridges.")
                init_complete = False
                neighbours = node['neighbours']
                if len(neighbours) == 1:
                    build_bridge(node['xy'], neighbours[0]['node'], idx, i_map, -node['capacity'], nrow, ncol, nodes, bridges)
                elif (node['capacity'] == (len(node['neighbours']) * MAX_BRIDGE_NUM)):
                    for neighbour in neighbours:
                        build_bridge(node['xy'], neighbour['node'], idx, i_map, -3, nrow, ncol, nodes, bridges)
                elif (node['value'] == (len(node['neighbours']) * MAX_BRIDGE_NUM)):
                    for neighbour in neighbours:
                        bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                        if bridge_idx > -1:
                            # print(f"OVERWRITING EXISTING BRIDGE:\n\t{bridges[bridge_idx]}\n")
                            build_bridge(node['xy'], neighbour['node'], idx, i_map, -3 - bridges[bridge_idx]['val'], nrow, ncol, nodes, bridges)
                        else:
                            build_bridge(node['xy'], neighbour['node'], idx, i_map, -3, nrow, ncol, nodes, bridges)
                else:
                    for neighbour in neighbours:
                        build_bridge(node['xy'], neighbour['node'], idx, i_map, -1, nrow, ncol, nodes, bridges)
                # Post-Lemma Pre-DFS map result
                # print_map(nrow, ncol, i_map)
                # print()
            # else:
                # print("Lemma unsatisfied\n")
    
    # Start dfs brutal search
    dfs_nodes = []
    incompleted_nodes = []
    for node in nodes:
        incompleted_nodes.append(node)
    dfs_nodes.append({
        'nodes': incompleted_nodes,
        'iter'  : 0,
    })

    dfs_bridges = []
    fixed_bridges = []
    for bridge in bridges:
        fixed_bridges.append(bridge)
    dfs_bridges.append({
        'bridges': fixed_bridges,
        'iter'  : 0,
    })
    # print(f"dfs nodes: {dfs_nodes}\ndfs bridges: {dfs_bridges}")
    sys.setrecursionlimit(100)
    tuning = False
    if (solve(i_map, nodes, bridges, nrow, ncol, 0, 0, tuning)):
        print("SUCCESS")
        print_map(nrow, ncol, i_map)
        print()
    # if (solve(i_map, dfs_nodes, dfs_bridges, nrow, ncol)):
    #     print("SUCCESS")

    # for node in nodes:
        # print(node)
    # for bridge in bridges:
        # print(bridge)
    return 0

def scan_map():
    text = []
    for line in sys.stdin:
        # print(f'line = {line}')
        row = []
        for ch in line:
            n = ord(ch)
            # print(f'ch = ${ch}, ch = ${n}')
            if n >= 48 and n <= 57:    # between '0' and '9'
                row.append(n - 48)
            elif n >= 97 and n <= 122: # between 'a' and 'z'
                row.append(n - 87)
            
            elif ch == '.':
                row.append(0)
        text.append(row)

    nrow = len(text)
    ncol = len(text[0])

    map = np.zeros((nrow,ncol),dtype=np.int32)
    for r in range(nrow):
        print(text[r])
        for c in range(ncol):
            map[r,c] = text[r][c]
    
    return nrow, ncol, map


if __name__ == '__main__':
    main()