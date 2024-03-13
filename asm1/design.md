### Assignment 1 – Bridge Puzzle

## Description and Restrictions:
- Each number represents an "island", while the dots represent the empty space (water) between the islands. Numbers larger than 9 are indicated by 'a' (10), 'b' (11) or 'c' (12). The aim is to connect all the islands with a network of bridges, satisfying these rules:
- all bridges must run horizontally or vertically
- bridges are not allowed to cross each other, or other islands
- there can be no more than three bridges connecting any pair of islands
- the total number of bridges connected to each island must be equal to the number on the island

# Definitions:
Define `MAX_BRIDGE_NUM` to be the maximum amount of bridges that could be built between nodes.  
In this assignment, `MAX_BRIDGE_NUM = 3`.  
Define `coordinates` to represent `(x, y)` which corresponds to the array index of the nodes.

# Constraints:
1. All nodes must exhaust their capacities, such that the amount of bridges built between a node and its connected nodes must be equal to their capacity.
2. Rows and Columns only. No diagonals.
3. Bridges do not cross. Hence for every bridge built, the map becomes slightly different in the way that:
    - For vertical bridges, nodes to the left `(x < x_0)` and nodes to the right `(x > x_0)` should reconsider valid options.
    - Similarly, nodes to the north `(y < y_0)` and nodes the south `(y > y_0)` should rerun check.

# Lemmas given the constraints:
- For node with 1 connectable nodes, connect and exhaust node capacity.
- For nodes with > 1 connectable nodes, we need to check the amount of valid connections it may establish.
    -   More specifically, for nodes with 2 connectable nodes, they must establish two connections if their capacity > `MAX_BRIDGE_NUM`,
    -   Similarly, this applies for nodes with capacity > `2 * MAX_BRIDGE_NUM` AND with 3 connectable nodes, 
    -   And finally, for nodes with capacity > `3 * MAX_BRIDGE_NUM`, they must connect with all 4 nodes on the same rows and columns.

# Potential solution:
```
for all nodes:
    check amount of paths available to other nodes on the same columns and rows, and apply the lemmas.
then either rerun this loop until no result could be obtained, or consciously update the a queue of nodes that should perform another check.
After the code above terminates, we are guaranteed to get a partially connected graph.  
Then we are to either utilise backtracking search for the remainder of the result, or give more procedural instructions to obtain the result.
```