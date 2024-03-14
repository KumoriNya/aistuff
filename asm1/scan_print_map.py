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
    print(f"Finding for {(x, y)} = {code[i_map[x,y]]}")

    neighbours = find_hori(x, y, i_map, ncol) + find_vert(x, y, i_map, nrow)
    print(f"All neighbours for {(x, y)} = {code[i_map[x,y]]}: {neighbours}")
    return neighbours

def check_lemma(node):
    print(f"Checking for {node}")
    return len(node['neighbours']) == 1 or (
        node['capacity']
        > ((len(node['neighbours']) - 1) * MAX_BRIDGE_NUM)
    )

def find_node(node):
    for idx, n in enumerate(nodes):
        if n['xy'] == node:
            return idx


def build_bridge(node_0, node_1, idx, i_map, val):
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
    idx_1 = find_node(node_1)
    nodes[idx]['capacity'] += val
    nodes[idx_1]['capacity'] += val
    return 0



def print_map(nrow, ncol, i_map):
    for r in range(nrow):
        for c in range(ncol):
            if (i_map[r,c] >= 0):
                print(code[i_map[r,c]],end="")
            else:
                print('B', end="")
        print()

def main():
    nrow, ncol, i_map = scan_map()
    for r in range(nrow):
        for c in range(ncol):
            if(i_map[r,c] > 0):
                nodes.append({
                    'xy': (r,c),
                    'capacity': i_map[r,c],
                    'neighbours': find_neighbours((r, c), i_map, nrow, ncol),
                    # 'neighbour_of': [],
                    'is_completed': False,
                    # 'bridges': []
                })
                # cur_node = nodes[len(nodes) - 1]

    print(f"Initialisation complete:")
    for node_idx, node in enumerate(nodes):
        new = []
        neighbours = node['neighbours']
        for neighbour in neighbours:
            neighbour_idx = find_node(neighbour)
            new.append({
                'node': neighbour,
                'position': neighbour_idx,
            })
            # nodes[neighbour_idx]['neighbour_of'].append({
            #     'node': node['xy'],
            #     'position': node_idx,
            # })

        node['neighbours'] = new
    for node in nodes:
        print(node)
    init_complete = True
    while (not init_complete):
        init_complete = True
        for idx, node in enumerate(nodes):
            print(f"Scanning, node #{idx}: {node}")
            if check_lemma(node):
                print(f"Node: {node['xy']} satisfies lemma. Building bridges.")
                init_complete = False
                neighbours = node['neighbours']
                if len(neighbours) == 1:
                    build_bridge(node['xy'], neighbours[0], idx, i_map, -node['capacity'])
                for neighbour in neighbours:
                    build_bridge(node['xy'], neighbour, idx, i_map, -1)
                    # node['bridges'].append({
                    #     'node': neighbour,
                    #     'val' : cur_node['capacity'],
                    # })
                print_map(nrow, ncol, i_map)
                print()
            else:
                print("Lemma unsatisfied")
    print_map(nrow, ncol, i_map)
    print()
    for node in nodes:
        print(node)
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