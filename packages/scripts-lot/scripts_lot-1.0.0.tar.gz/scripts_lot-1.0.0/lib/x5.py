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














# Lab4

import heapq
from collections import deque

def read_cube(filename):
    with open(filename, 'r') as f:
        cube = [list(map(int, line.strip().split())) for line in f]
    return cube

def is_valid(x, y, cube, visited):
    return 0 <= x < len(cube) and 0 <= y < len(cube[0]) and cube[x][y] != 1 and (x, y) not in visited

def bfs(cube):
    rows, cols = len(cube), len(cube[0])
    start, goal = (0, 0), (rows - 1, cols - 1)
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, cube, visited):
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return -1

def dfs(cube):
    rows, cols = len(cube), len(cube[0])
    start, goal = (0, 0), (rows - 1, cols - 1)
    stack = [(start, [start])]
    visited = set()

    while stack:
        (x, y), path = stack.pop()
        if (x, y) == goal:
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, cube, visited):
                visited.add((nx, ny))
                stack.append(((nx, ny), path + [(nx, ny)]))

    return -1

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(cube):
    rows, cols = len(cube), len(cube[0])
    start, goal = (0, 0), (rows - 1, cols - 1)
    pq = [(0, start, [start], 0)]
    visited = {}

    while pq:
        cost, (x, y), path, jumps = heapq.heappop(pq)

        if (x, y) == goal:
            return path

        if (x, y) in visited and visited[(x, y)] <= jumps:
            continue

        visited[(x, y)] = jumps

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                new_jumps = jumps + (1 if cube[nx][ny] == 2 else 0)
                heapq.heappush(pq, (cost + 1 + heuristic((nx, ny), goal), (nx, ny), path + [(nx, ny)], new_jumps))

    return -1

cube = read_cube('cube.txt')
print("BFS Path:", bfs(cube))
print("DFS Path:", dfs(cube))
print("A* Path:", a_star(cube))




#Lab5


def dijkstra(graph, start):
    # Initialize distances with infinity for all vertices except the start vertex
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0

    # Initialize previous vertices dictionary to reconstruct the path
    previous = {vertex: None for vertex in graph}

    unvisited = set(graph.keys())

    while unvisited:
        # Find the unvisited vertex with the smallest distance
        current = min(unvisited, key=lambda vertex: distances[vertex])

        # If the smallest distance is infinity, then remaining vertices are inaccessible
        if distances[current] == float('infinity'):
            break

        unvisited.remove(current)

        for neighbor, weight in graph[current].items():
            distance = distances[current] + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current

    return distances, previous

def reconstruct_path(previous, start, end):
    path = []
    current = end

    if previous[end] is None and end != start:
        return None

    while current is not None:
        path.append(current)
        current = previous[current]

    return path[::-1]

# Assumption: The graph is directed in the image
graph = {
    'A': {'B': 20, 'D': 80, 'G': 90},
    'B': {'F': 10},
    'C': {'H': 20},
    'D': {'C': 10, 'F': 40},
    'E': {'B': 50, 'G': 30},
    'F': {'C': 50},
    'G': {'A': 20, 'D': 20},
    'H': {}
}

start_vertex = 'A'
distances, previous = dijkstra(graph, start_vertex)

print(f"Shortest distances from vertex {start_vertex}:")
for vertex in sorted(distances.keys()):
    if vertex != start_vertex:
        path = reconstruct_path(previous, start_vertex, vertex)
        path_str = " -> ".join(path) if path else "No path exists"
        print(f"To {vertex}: Distance = {distances[vertex]}, Path = {path_str}")





# Lab6

"""
Tic Tac Toe Player
"""
import copy
import math
import random

X = "X"
O = "O"
D = "D"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def draw_board(board):
    print("-------------")
    for row in board:
        print("| ", end="")
        for cell in row:
            print(cell if cell else " ", end=" | ")
        print("\n-------------")

def player(board):
    count = sum(row.count(X) + row.count(O) for row in board)
    return O if count % 2 else X

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    return 1 if win == X else -1 if win == O else 0

def alpha_beta_pruning(board):
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v, best_action = -math.inf, None
        for action in actions(board):
            min_val, _ = min_value(result(board, action), alpha, beta)
            if min_val > v:
                v, best_action = min_val, action
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, best_action

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v, best_action = math.inf, None
        for action in actions(board):
            max_val, _ = max_value(result(board, action), alpha, beta)
            if max_val < v:
                v, best_action = max_val, action
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v, best_action

    return max_value(board, -math.inf, math.inf)[1] if player(board) == X else min_value(board, -math.inf, math.inf)[1]

def play_game():
    user = None
    board = initial_state()
    ai_turn = False
    print("Choose a player (X or O):")
    user = input().strip().upper()
    draw_board(board)
    while not terminal(board):
        playr = player(board)
        if playr == user:
            print("Enter the position to move (row,col):")
            i, j = map(int, input("Row, Col: ").split())
            if (i, j) in actions(board):
                board = result(board, (i, j))
            else:
                print("Invalid move. Try again.")
        else:
            print("AI is making a move...")
            action = alpha_beta_pruning(board)
            if action:
                board = result(board, action)
        draw_board(board)
    print("Game Over! Winner:", winner(board) if winner(board) else "Draw!")

if __name__ == "__main__":
    play_game()

import copy
import math
import random

X = "X"
O = "O"
D = "D"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def draw_board(board):
    print("-------------")
    for row in board:
        print("| ", end="")
        for cell in row:
            print(cell if cell else " ", end=" | ")
        print("\n-------------")

def player(board):
    count = sum(row.count(X) + row.count(O) for row in board)
    return O if count % 2 else X

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    win = winner(board)
    return 1 if win == X else -1 if win == O else 0

def alpha_beta_pruning(board):
    def max_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v, best_action = -math.inf, None
        for action in actions(board):
            min_val, _ = min_value(result(board, action), alpha, beta)
            if min_val > v:
                v, best_action = min_val, action
            alpha = max(alpha, v)
            if alpha >= beta:
                break
        return v, best_action

    def min_value(board, alpha, beta):
        if terminal(board):
            return utility(board), None
        v, best_action = math.inf, None
        for action in actions(board):
            max_val, _ = max_value(result(board, action), alpha, beta)
            if max_val < v:
                v, best_action = max_val, action
            beta = min(beta, v)
            if beta <= alpha:
                break
        return v, best_action

    return max_value(board, -math.inf, math.inf)[1] if player(board) == X else min_value(board, -math.inf, math.inf)[1]

def play_game():
    user = None
    board = initial_state()
    ai_turn = False
    print("Choose a player (X or O):")
    user = input().strip().upper()
    draw_board(board)
    while not terminal(board):
        playr = player(board)
        if playr == user:
            print("Enter the position to move (row,col):")
            i, j = map(int, input("Row, Col: ").split())
            if (i, j) in actions(board):
                board = result(board, (i, j))
            else:
                print("Invalid move. Try again.")
        else:
            print("AI is making a move...")
            action = alpha_beta_pruning(board)
            if action:
                board = result(board, action)
        draw_board(board)
    print("Game Over! Winner:", winner(board) if winner(board) else "Draw!")

if __name__ == "__main__":
    play_game()


