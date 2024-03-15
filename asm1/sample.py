def find_path(neighbour_fn,
  start,
  goal,
  visited,
  reachable = lambda pos: True,
  depth = 100000):
#The reachable function returns true if the given node is not blocked by a wall.

    """
    Returns the path between two nodes as a list of nodes using depth first search.
    If no path can be found, an empty list is returned.
    """

    if depth != 0:
        if goal == start:
            # If the start is also the goal, just return the start node
            if visited == [] or visited is None:
                return [start]
            return visited
    # Add the start node to visited

    if visited == [] or visited is None:
        visited.append(start)
    neighbours = neighbour_fn(start)

    for neighbour in neighbours:
        if neighbour in visited or not reachable(neighbour):
            pass
        # Recurse if neighbour is not visited and/or neighbour is reachable
        else:
            return_path = find_path(neighbour_fn, neighbour, goal, visited + [neighbour], reachable, depth - 1)
    # If the recursion returns empty list, the goal can't be found
    if return_path == [] or return_path is None:
        continue
    elif len(return_path) > 0:
        return return_path
    else:
    # If no path is found
        return []

target = [2,3,1,0]
sol = [0, 0, 0, 0]
def rec(arr, idx):
    print(f"Current index: {idx}\n\t{arr}")
    if (arr == target):
        return True
    if (idx == 4):
        print("\tFailed")
        return False
    for i in (range(0,4)):
        arr[idx] = i
        if rec(arr, idx+1):
            return True

    return False


print(sol)


rec(sol, 0)
print(sol)