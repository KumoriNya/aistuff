#!/usr/bin/python3
#************************************************************
#   hashi.py
#   Once the map is scanned, store all the islands in an array of dictionay,
#   The Island dictionary contains information about the islands':
#       1. coordinate(x,y); 
#       2. value of the island; 
#       3. capacity(value - # all connected bridges)
#       4. position (island's position in the array); 
#       5. neighbours: a list of {'neighbour_node_xy', 'position_in_array'}
#       6. is_completed: a boolean value indicating if an island is exhausted and satisfies constraints. 
#
#   Bridges are also stored in an array to keep track of the direction on the map,
#   which contains: 1. the coordinates of both ends of the bridge; 
#                   2. number of parallel bridges; 3. direction of the bridge (flat/vertical)
#   
#   Procedures:
#   Pre-Iterative Search processing: 
#       Given the constraints, we can deduce that 
#           1.  all islands with only 1 available neighbour island 
#               must connect with their neighbours with all their capacity;
#           2.  islands with capacity > (#neighbours - 1) * MaxBridgeNum(3) 
#               must connect with all their neighbours;
#           hence> 2.1. an island with capacity 6 with 2 neighbours must connect both with 3 bridges; 
#                       an island with capacity 9 with 3 neighbours must connect both with 3 bridges; 
#                       an island with capacity a / 12 with 4 neighbours must connect both with 3 bridges; 
#   The step about guarantees that all bridges built are necessary according to the constraints.
#
#   Algorithm: 
#       Idea: For all remaining unfinished nodes, try build 0 ~ 3 bridges with available neighbours
#   Pseudo-Code:
#     search():
#       An iterative DFS search. 
#       Base Case: if all neighbours of the current island have been searched, go to next island
#       Main Explore Loop: 
#           for i in [0, 1, 2, 3]: 
#               try build [No, 1, 2, 3] bridge(s) from the island to the current neighbour
#               calls search()  with the updated bridges info, nodes info,
#                               and increment the index for neighbour 
#                               such that it searches the next neighbour / island available 
#       Final Check:    if we hit this, we are at the end of a DFS tree / the top of the stack 
#                       thus we check if all nodes are finished(i.e. all their capacities are exhausted)
#                       if this is not satisfied, return False, and the (top - 1) stack continues to try 
#                       build a different amount of bridges until a valid map is built
#   Validation of the algo: Given we have at most 800 bridges to be built, 
#                           there is a maximum amount of 4 ^ 800 iterative checks to be done which is too large.
#                           Therefore a pre-iterative search processing is applied, but this still may leave a
#                           large amount of possibilities to be searched.
#                           To reduce the amount of iterative checks to be made, I've considered (but yet to implement)
#                           applying the Pre-Iterative search processing every time a new bridge is built.
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
bridge_tuning = True
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
    if (node['capacity'] == 0):          return -1
    if (len(node['neighbours']) == 0):  return -1
    # if ()
    if (len(node['neighbours']) == 1):                              return 0
    if node['value'] == 12:   return 1
    if node['capacity'] > ((len(node['neighbours']) - 1) * MAX_BRIDGE_NUM): return 2
    return -1

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

def bridge_uncolor_all():
    for bridge in bridges:
        bridge['is_new'] = False

# idx = idx of node_0
def build_bridge(node_0, node_1, idx, i_map, val, nrow, ncol, nodes, bridges):
    if bridge_tuning: print(f"--------------------------------------\nTrying to build the {len(bridges)}th connection: {-val} bridge(s) from {node_0} = {i_map[node_0]} to {node_1} = {i_map[node_1]}")
    bridge_uncolor_all()
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
        print(f"Error, bridge cannot be built")
        quit()
    # Organise the ends of the bridge
    ends = []
    if (x0 <= x1 and y0 <= y1):
        ends = [node_0, node_1]
    else:
        ends = [node_1, node_0]
    # Update bridge value or build new bridge
    bridge_idx = bridge_contains(node_0, node_1, bridges)
    #  -3 - bridges[bridge_idx]['val']
    pre_operation_bridge_val = 0
    if (bridge_idx != -1):
        pre_operation_bridge_val = bridges[bridge_idx]['val']
        bridges[bridge_idx]['val'] = val
        bridges[bridge_idx]['is_new'] = True
    else:
        bridges.append({
            'ends'  : ends,
            'val'   : val,
            'is_hor': x0==x1,
            'lemma_val':val,
            'is_new': True,
        })
    if bridge_tuning: print(f"Updating neighbours on the side of ends: {ends}")
    # Update affected nodes due to new bridge
    # TODO: add neighbours back if bridge destroyed
    if (x0==x1):
        for i in range(ends[0][1]+1,ends[1][1]):
            # print(f"{(x0, i)}")
            update_islands_perpendicular_to_bridge(True, x0, i, i_map, nrow, ncol, nodes, val)
    else:
    # print(ends[0][0]+1,ends[0][1])
        for i in range(ends[0][0]+1,ends[1][0]):
            # print(f"{(i, y0)}")
            update_islands_perpendicular_to_bridge(False, i, y0, i_map, nrow, ncol, nodes, val)
    if bridge_tuning: print(f"Checking point 1: ")

    # Update the node capacity
    idx_1 = find_node(node_1, nodes)
    nodes[idx]['capacity'] += (val- pre_operation_bridge_val)
    nodes[idx_1]['capacity'] += (val- pre_operation_bridge_val)

    # Update neighbours
    if (bridges[bridge_idx]['val'] == -3):
        remove_for_max_bridge(nodes[idx], nodes[idx_1])
        if bridge_tuning: print(f"Checking point 2:")
    if (nodes[idx]['capacity'] == 0):
        # Current node satisfied. Remove it from others list
        remove_current_node_in_neighbours_storage(nodes[idx])
        if bridge_tuning: print(f"Checking point 3:")
    if (nodes[idx_1]['capacity'] == 0):
        # Remove it from others list
        remove_current_node_in_neighbours_storage(nodes[idx_1])
        if bridge_tuning: print(f"Checking point 4:")
    if (val == 0):
        add_neighbours_back(nodes[idx], nodes[idx_1], nodes)
        if bridge_tuning: print(f"Checking point 5:")
    if bridge_tuning: print(f"Bridge({val}) from {node_0} = {i_map[node_0]} to {node_1} = {i_map[node_1]} built\nAffected nodes:\n\t{nodes[idx]}\n\t{nodes[idx_1]}\nBridge:\n\t{bridges[bridge_idx]}\n--------------------------------------\n")
    return 0

def update_islands_perpendicular_to_bridge(is_hor, x, y, i_map, nrow, ncol, nodes, bridge_val):
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
        if bridge_val < 0 and (info1 in node0['neighbours'] and info0 in node1['neighbours']):
            # Removes
            node0['neighbours'].remove(info1)
            node1['neighbours'].remove(info0)
            if bridge_tuning: 
                print(f"Due to bridge between built, Removed nodes {node_0} and {node_1} from their neighbours list")
                print(f"\t{node0}\n\t{node1}")
        elif bridge_val == 0 and (info1 not in node0['neighbours'] and info0 not in node1['neighbours']):
            node0['neighbours'].append(info1)
            node1['neighbours'].append(info0)
            if bridge_tuning: 
                print(f"Due to bridge between destroyed, Added nodes {node_0} and {node_1} to their neighbours list")
                print(f"\t{node0}\n\t{node1}")
            

def remove_for_max_bridge(node_0, node_1):
    info_0 = {
            'node': node_0['xy'],
            'position': node_0['position']
    }
    info_1 = {
            'node': node_1['xy'],
            'position': node_1['position']
    }
    if (info_0 in node_1['neighbours']):
        node_1['neighbours'].remove(info_0)
        if bridge_tuning: print(f"Removed {info_0} from {node_1}")
    else:
        print(f"THIS SHOULDNT HAPPEN.\n\tNeighbours: {node_1}")
        # quit()
    if (info_1 in node_0['neighbours']):
        node_0['neighbours'].remove(info_1)
        if bridge_tuning: print(f"Removed {info_1} from {node_0}")
    else:
        print(f"THIS SHOULDNT HAPPEN.\n\tNeighbours: {node_0}")
        # quit()

def add_neighbours_back(node_0, node_1, nodes):
    if bridge_tuning: print(f"======\nAdding neighbours back for\n\t{node_0}\nand\n\t{node_1}\n======")
    info_0 = {
        'node':     node_0['xy'],
        'position': node_0['position'],
    }
    info_1 = {
        'node':     node_1['xy'],
        'position': node_1['position'],
    }
    for bridge in bridges:
        # bridge not full capacity and node is one end of the bridge
        if (node_0['xy'] in bridge['ends'] and bridge['val'] > -3):
            # check if each other is free to add neighbour
            # obtain other end info
            other_end_xy = ()
            if bridge['ends'][0] == node_0['xy']:
                other_end_xy = bridge['ends'][1]
            else:
                other_end_xy = bridge['ends'][0]
            o_idx = find_node(other_end_xy, nodes)
            info_o = {
                'node':     other_end_xy,
                'position': o_idx,
            }
            # if other end is not in node's neighbours
            if (info_o not in node_0['neighbours']):
                other_end = nodes[o_idx]
                # and other end is not completed
                if other_end['capacity'] > 0 and info_0 not in other_end['neighbours']:
                    add_helper(info_0, other_end['neighbours'])
                    add_helper(info_o, node_0['neighbours'])
        if (node_1['xy'] in bridge['ends'] and bridge['val'] > -3):
            # check if each other is free to add neighbour
            # obtain other end info
            other_end_xy = ()
            if bridge['ends'][0] == node_1['xy']:
                other_end_xy = bridge['ends'][1]
            else:
                other_end_xy = bridge['ends'][0]
            o_idx = find_node(other_end_xy, nodes)
            info_o = {
                'node':     other_end_xy,
                'position': o_idx,
            }
            # if other end is not in node's neighbours
            if (info_o not in node_1['neighbours']):
                other_end = nodes[o_idx]
                # and other end is not completed
                if other_end['capacity'] > 0 and info_1 not in other_end['neighbours']:
                    add_helper(info_1, other_end['neighbours'])
                    add_helper(info_o, node_1['neighbours'])
    if (node_0['capacity'] > 0):
        node_0['is_completed'] = False
    if (node_1['capacity'] > 0):
        node_1['is_completed'] = False
    if bridge_tuning: print(f"======\nAdded neighbours back for\n\t{node_0}\nand\n\t{node_1}\n======")

def add_helper(info, lst):
    if len(lst) == 0:
        lst.append(info)
    else:
        for idx, neighbour in enumerate(lst):
            # print(f"In add helpers, neighbour:\n\t{neighbour}\n\t{info}")
            if (info['position'] < neighbour['position']):
                lst.insert(idx, info)
                return
        lst.append(info)

def remove_current_node_in_neighbours_storage(node):
    print(f"Removing\n\t{node}\n\tfrom:")
    self_info = {
            'node': node['xy'],
            'position': node['position']
        }
    for neighbour in node['neighbours']:
        neighbour_node = nodes[neighbour['position']]
        print(neighbour_node['neighbours'])
        if self_info in neighbour_node['neighbours']:
            neighbour_node['neighbours'].remove(self_info)
            print(f"Removed\n\t{node}\nfrom\n\t{neighbour_node}")
    node['neighbours'] = []
    node['is_completed'] = True
        
def code_bridge(is_hor, value):
    bridge_code = "-=E|\"#"
    code_idx = value - 1
    if (not is_hor):
        code_idx += 3
    # print color
    # if (is_new): print('\x1b[6;30;42m' + bridge_code[code_idx] + '\x1b[0m', end="")
    # if (is_new): print(bridge_code[code_idx], end="")
    # else: print(bridge_code[code_idx], end="")
    print(bridge_code[code_idx], end="")

def print_bridge(x, y, map_val):
    for bridge in bridges:
        start = bridge['ends'][0]
        end = bridge['ends'][1]
        if (bridge['is_hor']):
            if (x == start[0] and y > start[1] and y < end[1] and bridge['val'] == map_val):
                code_bridge(True, -bridge['val'])
                return True
        else:
            if (y == start[1] and x > start[0] and x < end[0] and bridge['val'] == map_val):
                code_bridge(False, -bridge['val'])
                return True
    return False

def print_map(nrow, ncol, i_map):
    # print("=====================")
    for r in range(nrow):
        for c in range(ncol):
            if (i_map[r,c] >= 0): print(code[i_map[r,c]],end="")
            else: print_bridge(r,c, i_map[r,c])
        print()
    # print("=====================")

def check_exhaustion(nodes):
    for node in nodes: 
        if (node['capacity'] != 0): return False
    return True

def check_remaining_nodes_availability(cur_idx):
    for i in (range(cur_idx, len(nodes))):
        if nodes[i]['capacity'] > 0 and len(nodes[i]['neighbours']) > 0:
            return True
    return False
#   nrow and ncol included for building bridges
    # Base Case:  All Exhausted => True
    #             All islands are traversedd but not exhausted => return False
    # Initialisation:
    #     Case:   Current node exhausted is exhausted => return recur(next node)
    #             If it's the first time iterating the current node (n_idx == -1), set it to be the latest neighbour for iteration
    #             If we have iterated all neighbours  => return recur(next node)
    #     ** Due to the behaviour of python list iteration and the nature of the operation of removing element from an array,
    #     ** For each node, we start trialing with its last available neighbour then iterate towards the first neighbour.
    # Iteration:
    #     Case:   Avoid downgrading lemma bridges.
    #             * This shouldn't happen, but avoid building from an exhausted island, or to an exhausted neighbour
    #             Build bridge with val = b, valid by (if (recur(next neighbour)): return True)
                
        
def recur(i_map, nodes, bridges, node_idx, neighbour_idx, is_test, nrow, ncol, non_reduce, stack_count):
    # Check returning conditions
    if (is_test):
        print(f"Enter #{stack_count} recursive at node index [{node_idx}] at its [{neighbour_idx}] th neighbour")
    # if is_test: print_map(nrow, ncol, i_map)
    if check_exhaustion(nodes): return True
    if node_idx == len(nodes):
        # All nodes traversed, but not exhausted -> no solution found
        if is_test: print(f"{stack_count} Traversed all nodes and not succeeded. Current Status:")
        if is_test: print_map(nrow, ncol, i_map)
        return False
    # Add an additional check for nodes after the current idx, whether it's still meaningful to iterate based on the allocation
    if not check_remaining_nodes_availability(node_idx):
        return False
    
    
    node = nodes[node_idx]
    if is_test: print(f"Stack #{stack_count}, node#{node['position']}: {node}")
    if node['capacity'] == 0:
        # Early end recursive due to current stack exhausts the current node
        if recur(i_map, nodes, bridges, node_idx + 1, -1, is_test, nrow, ncol, non_reduce, stack_count + 1):
            return True
    neighbours = node['neighbours']
    # This indicates the current allocation of resource leaves one node unsatisfied. Thus this allocation must be wrong 
    if is_test: print(f"Stack #{stack_count}, neighbours: {neighbours}")
    if (len(neighbours) == 0 and node['capacity'] > 0):
        if is_test: print(f"THIS SHOULD only come out in invalid tests, {node}")
        return False
    elif (len(neighbours) == 0 and node['capacity'] == 0):
        if is_test: print(F"Stack#{stack_count} satisfied node#{node['position']}: {node} during iteration call")
        # Dont return straightaway because earlier stack might not be satisfied, and we need to 
        if (recur(i_map, nodes, bridges, node_idx + 1, -1, is_test, nrow, ncol, non_reduce, stack_count + 1)): return True
    if neighbour_idx == -1:
        neighbour_idx = len(neighbours)
    # Bridge established in iteration call satisfied multiple neighbours
    while (neighbour_idx > len(neighbours)):
        neighbour_idx -= 1
    if neighbour_idx == 0:
        # Indicate that current neighbour has all been iterated.
        return recur(i_map, nodes, bridges, node_idx + 1, -1, is_test, nrow, ncol, non_reduce, stack_count + 1)
    # if is_test: print(f"NIDX #{stack_count}, {neighbour_idx}")
    neighbour = neighbours[neighbour_idx - 1]
    if is_test: print(f"Stack #{stack_count}, neighbour#{neighbour_idx}: {neighbour}")
    
    # If no available neighbour, return False?

    # Only build forward
    if is_test: print(f"Recursively checking #{stack_count} at node index [{node_idx}] at its [{neighbour_idx - 1}] th neighbour\n\tNode: {nodes[node_idx]}")
    # if (neighbour['position'] < node['position']):
    if (node['position'] < neighbour['position']):
        for build_bridge_val in reversed(range(-3, 0)):
            bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
            neighbour_node = nodes[neighbour['position']]
            # Try Build Bridge Block
            # Avoid downgrading lemma bridge values
            if (bridge_idx != -1 and bridge_idx < non_reduce):
                if (bridges[bridge_idx]['lemma_val'] <= build_bridge_val):
                    print(f"Failed Trying to {build_bridge_val} build(s) at #{stack_count} stack since {bridge_idx} < {non_reduce}.")
                    pass
                else:
                    if (neighbour_node['capacity'] == 0 or node['capacity'] == 0):
                        if (recur(i_map, nodes, bridges, node_idx + 1, -1, is_test, nrow, ncol, non_reduce, stack_count + 1)): return True
                    else:
                        print(f"Stack #{stack_count} Upgrading lemma bridge {bridges[bridge_idx]}")
                        # build_bridge(node['xy'], neighbour['node'], node_idx, i_map, 0, nrow, ncol, nodes, bridges)
                        # build_bridge(node['xy'], neighbour['node'], node_idx, i_map, bridges[bridge_idx]['lemma_val'], nrow, ncol, nodes, bridges)
                        build_bridge(node['xy'], neighbour['node'], node_idx, i_map, build_bridge_val, nrow, ncol, nodes, bridges)
                        if (is_test): 
                            print_map(nrow, ncol, i_map)
                            print(f"Built {int(-build_bridge_val)} bridge from {node['xy']} to {neighbour['node']}\n==================================================================\n")
            else:
                # Neighbour exhausted by bridge building from previous iteration
                # Since current neighbour is exhausted => go to next neighbour
                # Neighbours all iterated (i.e. a bridge from the current island to all neighbours with at least 0 bridges)
                # If current node not exhausted, try to build bridge with the next available neighbour
                if (neighbour_node['capacity'] == 0 or node['capacity'] == 0):
                    # During iteration, current neighbour exhausted or node exhausted
                    #   => recur on next node
                    if (recur(i_map, nodes, bridges, node_idx + 1, -1, is_test, nrow, ncol, non_reduce, stack_count + 1)): 
                        return True
                # Node exhausted from previous iteration on neighbours => go to next node
                else:
                    if is_test: print(f"Stack #{stack_count} Trying to {-build_bridge_val} build(s) at #{stack_count} stack from {node['xy']} to {neighbour['node']}.")
                    build_bridge(node['xy'], neighbour['node'], node_idx, i_map, build_bridge_val, nrow, ncol, nodes, bridges)
                    if (is_test): 
                        print_map(nrow, ncol, i_map)
                        print(f"Built {int(-build_bridge_val)} bridge from {node['xy']} to {neighbour['node']}\n==================================================================\n")
            # Bridges built, See if this works
            if (recur(i_map, nodes, bridges, node_idx, neighbour_idx - 1, is_test, nrow, ncol, non_reduce, stack_count + 1)): return True
            elif build_bridge_val == -3:
                build_bridge(node['xy'], neighbour['node'], node_idx, i_map, 0, nrow, ncol, nodes, bridges)
                if (bridges[bridge_idx]['lemma_val'] < 0):
                    build_bridge(node['xy'], neighbour['node'], node_idx, i_map, bridges[bridge_idx]['lemma_val'], nrow, ncol, nodes, bridges)
    else:
        if (recur(i_map, nodes, bridges, node_idx, neighbour_idx - 1, is_test, nrow, ncol, non_reduce, stack_count + 1)): return True
    if (is_test):
        print(f"Stack #{stack_count} failed [{node_idx}] at its [{neighbour_idx}] th neighbour")
    return False

# only_map = False
def main():
    # if (len(sys.argv)) == 2:
    #     # Write to file
    #     pass
    # else:
    #     only_map = True
    nrow, ncol, i_map = scan_map()
    # Get islands/nodes
    for r in range(nrow):
        for c in range(ncol):
            map_v = i_map[r,c]
            if(map_v > 0):
                nodes.append({
                    'xy': (r,c),
                    'value':    map_v,
                    'capacity': map_v,
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
        node['neighbours'] = []
        for info in new:
            add_helper(info, node['neighbours'])
        
    
    # for node in nodes:
    #     print(node)
    tuning = True

    # print(f"Initialisation complete:")
    # for node in nodes:
    #     print(node)
    # For all nodes, try apply the lemma to link islands that must be connected before applying other search strategies
    init_complete = False
    check_lemma_ = True
    lmc = -1
    if (check_lemma_):
        print("Start checking lemma")
        while (not init_complete):
            lmc = lmc + 1
            # if (lmc == 5): break
            init_complete = True
            print(f"\n\nIterating\n\n")
            for idx, node in enumerate(nodes):
                # May also want to update check_lemma to iterate using the list of dict
                if check_lemma(node) > -1:
                    print(f"Node: {node['xy']} = {node['value']} satisfies lemma {check_lemma(node)}; {node} Building bridges.")
                    init_complete = False
                    neighbours = node['neighbours']
                    if len(neighbours) == 1:
                        bridge_idx = bridge_contains(node['xy'], neighbours[0]['node'], bridges)
                        if (bridge_idx > -1):
                            # build_bridge(node['xy'], neighbours[0]['node'], idx, i_map, 0, nrow, ncol, nodes, bridges)
                            new_lv = -node['capacity']+bridges[bridge_idx]['val']
                            print(f"new_lv = {new_lv}")
                            build_bridge(node['xy'], neighbours[0]['node'], idx, i_map, new_lv, nrow, ncol, nodes, bridges)
                            bridges[bridge_idx]['lemma_val'] = new_lv
                        else:
                            build_bridge(node['xy'], neighbours[0]['node'], idx, i_map, -node['capacity'], nrow, ncol, nodes, bridges)
                    elif (node['capacity'] == (len(node['neighbours']) * MAX_BRIDGE_NUM)):
                        print(f"FOUND {node['value']} at {node['xy']} with neighbours: {neighbours}")
                        for i in reversed(range(0, len(node['neighbours']))):
                            neighbour = neighbours[i]
                            build_bridge(node['xy'], neighbour['node'], idx, i_map, -3, nrow, ncol, nodes, bridges)
                            bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                            bridge = bridges[bridge_idx]
                            bridge['lemma_val'] = -3
                            if node['value'] == 12:
                                print_map(nrow, ncol, i_map)
                                print()
                    # elif (node['value'] == (len(node['neighbours']) * MAX_BRIDGE_NUM)):
                    #     for neighbour in neighbours:
                    #         bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                    #         build_bridge(node['xy'], neighbour['node'], idx, i_map, -3, nrow, ncol, nodes, bridges)
                    else:
                        available_val = node['capacity']
                        # Case for the right most 8 on the 6th row (5, 16)
                        non_exhausted_bridge_val = 0
                        neighbours_capacity_excluding_cur_bridges = []
                        built_bridges = []
                        for neighbour in neighbours:
                            bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                            if (bridge_idx > -1):
                                b_val = bridges[bridge_idx]['val']
                                non_exhausted_bridge_val += b_val
                                n = nodes[neighbour['position']]
                                neighbours_capacity_excluding_cur_bridges.append({
                                    'node': neighbour['node'],
                                    'capa': n['capacity'] - b_val,
                                })
                        tmp = available_val - non_exhausted_bridge_val
                        if tmp == len(neighbours) * MAX_BRIDGE_NUM:
                            # WE SHOULD BE ABLE TO BUILD MULTIPLE 3 BRIDGES HERE
                            if tuning: print("CASE AAA")
                            while (tmp > 3):
                                tmp -= 3
                            for neighbour in neighbours_capacity_excluding_cur_bridges:
                                build_val = -tmp
                                if tuning: print(f"Try to build {tmp} or {neighbour['capa']} bridges from {node['xy']} to {neighbour['node']}")
                                if neighbour['capa'] < tmp: build_val = -neighbour['capa']
                                build_bridge(node['xy'], neighbour['node'], idx, i_map, build_val, nrow, ncol, nodes, bridges)
                                bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                                bridge = bridges[bridge_idx]
                                if (bridge['lemma_val'] > build_val): bridge['lemma_val'] = build_val
                        elif tmp < len(neighbours) * MAX_BRIDGE_NUM:
                            if tuning: print("CASE BBB")
                            while (tmp > 3):
                                tmp -= 3
                            for neighbour in neighbours_capacity_excluding_cur_bridges:
                                build_val = -tmp
                                if tuning: print(f"Try to build {tmp} or {neighbour['capa']} bridges from {node['xy']} to {neighbour['node']}")
                                if neighbour['capa'] < tmp: build_val = -neighbour['capa']
                                build_bridge(node['xy'], neighbour['node'], idx, i_map, build_val, nrow, ncol, nodes, bridges)
                                bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                                bridge = bridges[bridge_idx]
                                if (bridge['lemma_val'] > build_val): bridge['lemma_val'] = build_val
                        else:
                            if tuning: print(f"THIS SHOULDNT HAPPEN. CHECK WHY LEMMA WORKS")
                            
                        while (available_val > 3):
                            available_val -= 3
                        for neighbour in neighbours:
                            if tuning: print("CASE CCC")
                            build_val = -available_val
                            n = nodes[neighbour['position']]
                            if tuning: print(f"Try to build {available_val} or {n['capacity']} bridges from {node['xy']} to {neighbour['node']}")
                            if n['capacity'] < available_val: build_val = -n['capacity']
                            build_bridge(node['xy'], neighbour['node'], idx, i_map, build_val, nrow, ncol, nodes, bridges)
                            bridge_idx = bridge_contains(node['xy'], neighbour['node'], bridges)
                            bridge = bridges[bridge_idx]
                            if (bridge['lemma_val'] > build_val): bridge['lemma_val'] = build_val
                
                
                # Post-Lemma Pre-DFS map result
            print(f"Lemma iteration {lmc}")
            # print_map(nrow, ncol, i_map)
            # print()
        print("finished checking lemma")
        print_map(nrow, ncol, i_map)
        print()
            # else:
                # print("Lemma unsatisfied\n")
    

    
    for node_idx, node in enumerate(nodes):
        neighbours = node['neighbours']
        for neighbour in neighbours:
            if (bridge_contains(node['xy'], neighbour['node'], bridges) < 0):
                build_bridge(node['xy'], neighbour['node'], node_idx, i_map, 0, nrow, ncol, nodes, bridges)
    # Start dfs brutal search
    # print(f"dfs nodes: {dfs_nodes}\ndfs bridges: {dfs_bridges}")
    sys.setrecursionlimit(1000)
    # solve(i_map, nodes, bridges, nrow, ncol, 0, 0, tuning)
    print("INITIALISATION COMPLETE")
    recur(i_map, nodes, bridges, 0, -1, tuning, nrow, ncol, len(bridges), 0)
    print_map(nrow, ncol, i_map)
    # if (solve(i_map, dfs_nodes, dfs_bridges, nrow, ncol)):
    #     print("SUCCESS")

    for node in nodes:
        print(node)
    for bridge in bridges:
        print(bridge)
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
        # print(text[r])
        for c in range(ncol):
            map[r,c] = text[r][c]
    
    return nrow, ncol, map


if __name__ == '__main__':
    main()