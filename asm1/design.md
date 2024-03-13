### Assignment 1 – Bridge Puzzle

## Description and Restrictions:
- Each number represents an "island", while the dots represent the empty space (water) between the islands. Numbers larger than 9 are indicated by 'a' (10), 'b' (11) or 'c' (12). The aim is to connect all the islands with a network of bridges, satisfying these rules:
- all bridges must run horizontally or vertically
- bridges are not allowed to cross each other, or other islands
- there can be no more than three bridges connecting any pair of islands
- the total number of bridges connected to each island must be equal to the number on the island

# Problems:
- For node with 1 connectable nodes, connect and exhaust node capacity.
- For nodes with > 1 connectable nodes, we need to check the amount of valid connections it may establish.
    -   More specifically, 