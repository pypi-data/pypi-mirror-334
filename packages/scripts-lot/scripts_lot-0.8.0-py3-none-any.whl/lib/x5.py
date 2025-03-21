from collections import deque

def bfs(graph, start):
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            queue.extend(graph[node] - visited)

# Example Usage
graph = {
    'A': {'B', 'C'},
    'B': {'A', 'D', 'E'},
    'C': {'A', 'F'},
    'D': {'B'},
    'E': {'B', 'F'},
    'F': {'C', 'E'}
}

print("BFS Traversal:")
bfs(graph, 'A')











def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    if node not in visited:
        print(node, end=" ")
        visited.add(node)
        for neighbor in graph[node]:
            dfs_recursive(graph, neighbor, visited)

print("\nDFS Recursive Traversal:")
dfs_recursive(graph, 'A')








def dfs_iterative(graph, start):
    visited = set()
    stack = [start]

    while stack:
        node = stack.pop()
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            stack.extend(graph[node] - visited)

print("\nDFS Iterative Traversal:")
dfs_iterative(graph, 'A')










import heapq

def a_star(graph, start, goal, heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic[start]

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor, cost in graph[current].items():
            tentative_g_score = g_score[current] + cost
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic[neighbor]
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None

# Example Usage
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'D': 2, 'E': 5},
    'C': {'A': 4, 'F': 3},
    'D': {'B': 2},
    'E': {'B': 5, 'F': 1},
    'F': {'C': 3, 'E': 1}
}
heuristic = {'A': 7, 'B': 6, 'C': 2, 'D': 3, 'E': 1, 'F': 0}

print("\nA* Path from A to F:", a_star(graph, 'A', 'F', heuristic))



















import heapq

def dijkstra(graph, start):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Example Usage
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'D': 2, 'E': 5},
    'C': {'A': 4, 'F': 3},
    'D': {'B': 2},
    'E': {'B': 5, 'F': 1},
    'F': {'C': 3, 'E': 1}
}

print("\nDijkstra Shortest Paths from A:", dijkstra(graph, 'A'))



# Simple MinMax
import math

def minimax(depth, node_index, is_max, scores, height):
    # Base case: if we have reached the leaf node
    if depth == height:
        return scores[node_index]
    
    if is_max:
        return max(
            minimax(depth + 1, node_index * 2, False, scores, height),
            minimax(depth + 1, node_index * 2 + 1, False, scores, height)
        )
    else:
        return min(
            minimax(depth + 1, node_index * 2, True, scores, height),
            minimax(depth + 1, node_index * 2 + 1, True, scores, height)
        )

# Example usage
if __name__ == "__main__":
    scores = [3, 5, 2, 9, 12, 5, 23, 23]  # Terminal values of leaf nodes
    height = math.log2(len(scores))  # Calculate tree height
    
    optimal_value = minimax(0, 0, True, scores, int(height))
    print("The optimal value is:", optimal_value)




# Minmax For TicTacToe 
import math

def minimax(depth, node_index, is_max, scores, height):
    # Base case: if we have reached the leaf node
    if depth == height:
        return scores[node_index]
    
    if is_max:
        return max(
            minimax(depth + 1, node_index * 2, False, scores, height),
            minimax(depth + 1, node_index * 2 + 1, False, scores, height)
        )
    else:
        return min(
            minimax(depth + 1, node_index * 2, True, scores, height),
            minimax(depth + 1, node_index * 2 + 1, True, scores, height)
        )

# Tic-Tac-Toe Example
def evaluate(board):
    # Check rows, columns, and diagonals for a win
    for row in board:
        if row[0] == row[1] == row[2]:
            return 10 if row[0] == 'X' else -10 if row[0] == 'O' else 0
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col]:
            return 10 if board[0][col] == 'X' else -10 if board[0][col] == 'O' else 0
    
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        return 10 if board[1][1] == 'X' else -10 if board[1][1] == 'O' else 0
    
    return 0

def is_moves_left(board):
    for row in board:
        for cell in row:
            if cell == '_':
                return True
    return False

def minimax_tic_tac_toe(board, depth, is_max):
    score = evaluate(board)
    
    if score == 10 or score == -10:
        return score
    
    if not is_moves_left(board):
        return 0
    
    if is_max:
        best = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'X'
                    best = max(best, minimax_tic_tac_toe(board, depth + 1, False))
                    board[i][j] = '_'
        return best
    else:
        best = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = 'O'
                    best = min(best, minimax_tic_tac_toe(board, depth + 1, True))
                    board[i][j] = '_'
        return best

# Example Tic-Tac-Toe board
if __name__ == "__main__":
    board = [
        ['X', 'O', 'X'],
        ['O', 'O', 'X'],
        ['_', '_', '_']
    ]
    print("Optimal Tic-Tac-Toe Move Value:", minimax_tic_tac_toe(board, 0, True))

