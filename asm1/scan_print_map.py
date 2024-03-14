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
        # print(f"Checking {(i, y)}")
        if (i_map[i][y] != 0):
            # print(f"Closest island for {(x,y)} = {i_map[x][y]} in adscending vertical order (top of) is {(i, y)} = {i_map[i][y]}")
            hori_neightbours.append((i, y))
            break
    for i in range(x + 1, nrow):
        if (i_map[i][y] != 0):
            # print(f"Closest island for {(x,y)} = {i_map[x][y]} in descending vertical order (bottom of) is {(i, y)} = {i_map[i][y]}")
            hori_neightbours.append((i, y))
            break
    return hori_neightbours

def find_hori(x, y, i_map, ncol):
    vert_neightbours = []
    for i in reversed(range(0, y)):
        # print(f"Checking {(x, i)}")
        if (i_map[x][i] != 0):
            # print(f"Closest island for {(x,y)} = {i_map[x][y]} in adscending horizontal order (left of) is {(x, i)} = {i_map[x][i]}")
            vert_neightbours.append((x, i))
            break
    for i in range(y + 1, ncol):
        # print(f"Checking {(x, i)}")
        if (i_map[x][i] != 0):
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
    return len(node['neighbours']) == 1 or (node['capacity'] > len(node['neighbours'] * MAX_BRIDGE_NUM))

def main():
    nrow, ncol, i_map = scan_map()
    for r in range(nrow):
        for c in range(ncol):
            if(i_map[r,c] > 0):
                nodes.append({
                    'xy': (r,c),
                    'capacity': i_map[r,c],
                    'neighbours': find_neighbours((r, c), i_map, nrow, ncol),
                    'bridges': []
                })
                cur_node = nodes[len(nodes) - 1]
                if check_lemma(cur_node):
                    neighbours = cur_node['neighbours']
                    for neighbour in neighbours:
                        cur_node['bridges'].append({
                            'node': neighbour,
                            'val' : cur_node['capacity'],
                        })
        print()
    for r in range(nrow):
        for c in range(ncol):
            print(code[i_map[r,c]],end="")
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