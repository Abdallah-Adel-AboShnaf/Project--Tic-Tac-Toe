from tkinter import *
import time

size = 3
players = {"player1": "X", "player2": "O"}
selected_algorithm = "minimax"

def board_to_1d(board):
    return [board[i][j] for i in range(size) for j in range(size)]

def new_game():
    global board, player
    board = [[0 for _ in range(size)] for _ in range(size)]
    player = players["player1"]
    label.config(text=f"{player}'s turn")
    algorithm_menu_widget.config(state=NORMAL)
    for row in range(size):
        for column in range(size):
            buttons[row][column].config(text=" ", state=NORMAL, bg="#F0F0F0")

def mark_square(row, column, player_symbol):
    board[row][column] = player_symbol

def next_turn(row, column):
    global player
    if buttons[row][column]["text"] == " " and not check_winner():
        buttons[row][column]['text'] = player
        mark_square(row, column, player)

        algorithm_menu_widget.config(state=DISABLED)

        if not check_winner():
            player = players["player2"]
            label.config(text="Player 2 thinking...")
            window.after(500, best_move)
        else:
            declare_winner()

def declare_winner():
    result = check_winner()
    if result == players["player1"]:
        label.config(text=f"{players['player1']} wins!")
    elif result == players["player2"]:
        label.config(text=f"{players['player2']} wins!")
    elif result == "Tie":
        label.config(text="It's a Tie!")
    disable_buttons()

def disable_buttons():
    for row in range(size):
        for column in range(size):
            buttons[row][column].config(state=DISABLED)

def check_winner():
    for row in range(size):
        if board[row][0] == board[row][1] == board[row][2] != 0:
            return board[row][0]
    for column in range(size):
        if board[0][column] == board[1][column] == board[2][column] != 0:
            return board[0][column]
    if board[0][0] == board[1][1] == board[2][2] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != 0:
        return board[0][2]
    if is_board_full():
        return "Tie"
    return None

def is_board_full():
    return all(board[row][column] != 0 for row in range(size) for column in range(size))

def minimax(board, depth, is_maximizing):
    result = check_winner()
    if result == players["player2"]:
        return 1
    elif result == players["player1"]:
        return -1
    elif result == "Tie":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player2"]
                    score = minimax(board, depth + 1, False)
                    board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player1"]
                    score = minimax(board, depth + 1, True)
                    board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score

def minimax_alpha_beta(board, depth, is_maximizing, alpha, beta):
    result = check_winner()
    if result == players["player2"]:
        return 1
    elif result == players["player1"]:
        return -1
    elif result == "Tie":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player2"]
                    score = minimax_alpha_beta(board, depth + 1, False, alpha, beta)
                    board[row][column] = 0
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player1"]
                    score = minimax_alpha_beta(board, depth + 1, True, alpha, beta)
                    board[row][column] = 0
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score

def canonical_form(board):
    transforms = []
    transforms.append(board)
    transforms.append([list(row) for row in zip(*board[::-1])])
    transforms.append([row[::-1] for row in board[::-1]])
    transforms.append([list(row) for row in zip(*board)][::-1])
    transforms.append([row[:] for row in board[::-1]])
    transforms.append([row[::-1] for row in board])
    transforms.append([list(row) for row in zip(*board)])
    transforms.append([list(row) for row in zip(*board[::-1])][::-1])
    return min(transforms, key=lambda x: str(x))

def minimax_symmetry(board, depth, is_maximizing, visited=None):
    if visited is None:
        visited = set()
    result = check_winner()
    if result == players["player2"]:
        return 1
    elif result == players["player1"]:
        return -1
    elif result == "Tie":
        return 0
    canonical = canonical_form(board)
    board_key = tuple(tuple(row) for row in canonical)
    if board_key in visited:
        return 0
    visited.add(board_key)
    if is_maximizing:
        best_score = -float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player2"]
                    score = minimax_symmetry(board, depth + 1, False, visited.copy())
                    board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player1"]
                    score = minimax_symmetry(board, depth + 1, True, visited.copy())
                    board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score

def heuristic_winning_blocking(board_1d, Player2, Player1):
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    score = 0
    for line in winning_lines:
        ai_count = sum(1 for i in line if board_1d[i] == Player2)
        human_count = sum(1 for i in line if board_1d[i] == Player1)
        if ai_count > 0 and human_count == 0:
            score += 10 ** ai_count
        if human_count > 0 and ai_count == 0:
            score -= 10 ** human_count
    return score

def heuristic_with_fork_detection(board_1d, Player2, Player1):
    winning_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    score = 0
    ai_two_mark_lines = 0
    human_two_mark_lines = 0
    for line in winning_lines:
        ai_count = sum(1 for i in line if board_1d[i] == Player2)
        human_count = sum(1 for i in line if board_1d[i] == Player1)
        if ai_count > 0 and human_count == 0:
            score += 10 ** ai_count
            if ai_count == 2:
                ai_two_mark_lines += 1
        if human_count > 0 and ai_count == 0:
            score -= 10 ** human_count
            if human_count == 2:
                human_two_mark_lines += 1
    if ai_two_mark_lines >= 2:
        score += 1000
    if human_two_mark_lines >= 2:
        score -= 1000
    return score

def minimax_with_winning_blocking(board, depth, is_maximizing):
    result = check_winner()
    if result == players["player2"]:
        return 100
    elif result == players["player1"]:
        return -100
    elif result == "Tie":
        return 0
    if depth >= 4:
        return heuristic_winning_blocking(board_to_1d(board), players["player2"], players["player1"])
    if is_maximizing:
        best_score = -float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player2"]
                    score = minimax_with_winning_blocking(board, depth + 1, False)
                    board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player1"]
                    score = minimax_with_winning_blocking(board, depth + 1, True)
                    board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score

def minimax_with_fork_detection(board, depth, is_maximizing):
    result = check_winner()
    if result == players["player2"]:
        return 100
    elif result == players["player1"]:
        return -100
    elif result == "Tie":
        return 0
    if depth >= 4:
        return heuristic_with_fork_detection(board_to_1d(board), players["player2"], players["player1"])
    if is_maximizing:
        best_score = -float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player2"]
                    score = minimax_with_fork_detection(board, depth + 1, False)
                    board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(size):
            for column in range(size):
                if board[row][column] == 0:
                    board[row][column] = players["player1"]
                    score = minimax_with_fork_detection(board, depth + 1, True)
                    board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score
    
def heuristic_positional_mobility(board_1d, Player2, Player1):
    score = 0
    
    # 1. Center Control (Most important square)
    if board_1d[4] == Player2: score += 3
    elif board_1d[4] == Player1: score -= 3
    
    # 2. Corner Control (Next best squares)
    corners = [0, 2, 6, 8]
    for pos in corners:
        if board_1d[pos] == Player2: score += 2
        elif board_1d[pos] == Player1: score -= 2
    
    # 3. Mobility (Number of possible next moves)
    p2_moves = sum(1 for cell in board_1d if cell == 0)  # Count empty cells
    p1_moves = p2_moves  # Same for opponent
    
    # If AI has more moves, reward; if opponent does, penalize
    score += (p2_moves - p1_moves) * 0.5
    
    # 4. Immediate win/loss (still crucial)
    winning_lines = [[0,1,2], [3,4,5], [6,7,8], [0,3,6], [1,4,7], [2,5,8], [0,4,8], [2,4,6]]
    for line in winning_lines:
        p2 = sum(1 for i in line if board_1d[i] == Player2)
        p1 = sum(1 for i in line if board_1d[i] == Player1)
        if p2 == 3: return 100  # AI wins
        if p1 == 3: return -100  # Opponent wins
        if p2 == 2 and p1 == 0: score += 5  # Potential win
        if p1 == 2 and p2 == 0: score -= 5  # Potential loss
    
    return score

def best_move():
    start_time = time.time()
    best_score = -float('inf')
    move = (-1, -1)
    for row in range(size):
        for column in range(size):
            if board[row][column] == 0:
                board[row][column] = players["player2"]
                if selected_algorithm == "minimax":
                    score = minimax(board, 0, False)
                elif selected_algorithm == "minimax_alpha-beta":
                    score = minimax_alpha_beta(board, 0, False, -float('inf'), float('inf'))
                elif selected_algorithm == "minimax_symmetry":
                    score = minimax_symmetry(board, 0, False)
                elif selected_algorithm == "heuristic_winning_blocking":
                    score = heuristic_winning_blocking(board_to_1d(board), players["player2"], players["player1"])
                elif selected_algorithm == "heuristic_with_fork_detection":
                    score = heuristic_with_fork_detection(board_to_1d(board), players["player2"], players["player1"])
                elif selected_algorithm == "minimax_with_winning_blocking":
                    score = minimax_with_winning_blocking(board, 0, False)
                elif selected_algorithm == "minimax_with_fork_detection":
                    score = minimax_with_fork_detection(board, 0, False)
                elif selected_algorithm == "heuristic_positional_mobility":
                    score = heuristic_positional_mobility(board_to_1d(board), players["player2"], players["player1"])
                else:
                    score = 0
                board[row][column] = 0
                if score > best_score:
                    best_score = score
                    move = (row, column)

    if move != (-1, -1):
        row, column = move
        buttons[row][column]['text'] = players["player2"]
        mark_square(row, column, players["player2"])
        elapsed = round(time.time() - start_time, 3)
        if check_winner():
            declare_winner()
        else:
            global player
            player = players["player1"]
            label.config(text=f"Player 1 turn | AI took {elapsed} sec")

def set_algorithm(value):
    global selected_algorithm
    selected_algorithm = value

# GUI Setup
window = Tk()
window.title("Tic-Tac-Toe AI")
window.configure(bg="#F8F9FA")

label = Label(text=f"{players['player1']}'s Turn", font=("Segoe UI", 24), bg="#F8F9FA", fg="#333")
label.pack(pady=10)

menu_frame = Frame(window, bg="#F8F9FA")
menu_frame.pack()

Label(menu_frame, text="AI Algorithm:", font=("Segoe UI", 14), bg="#F8F9FA").pack(side=LEFT)
algorithm_var = StringVar(window)
algorithm_var.set("minimax")
algorithm_menu_widget = OptionMenu(menu_frame, algorithm_var,
                                "minimax", "minimax_alpha-beta", "minimax_symmetry",
                                "heuristic_winning_blocking", "heuristic_with_fork_detection",
                                "minimax_with_winning_blocking", "minimax_with_fork_detection", 
                                "heuristic_positional_mobility",
                                command=set_algorithm)
algorithm_menu_widget.config(font=("Segoe UI", 12), bg="#E9ECEF", relief=FLAT)
algorithm_menu_widget.pack(side=LEFT, padx=5)

reset_button = Button(window, text="New Game", font=("Segoe UI", 14), bg="#007BFF", fg="white",
                    relief=FLAT, padx=10, pady=5, command=new_game)
reset_button.pack(pady=10)

frame = Frame(window, bg="#F8F9FA")
frame.pack()

buttons = [[None for _ in range(size)] for _ in range(size)]
for row in range(size):
    for column in range(size):
        btn = Button(frame, text=" ", font=("Segoe UI", 36), width=5, height=2,
                    bg="#FFFFFF", fg="#333", relief=RAISED,
                    command=lambda row=row, column=column: next_turn(row, column))
        btn.grid(row=row, column=column, padx=5, pady=5)
        buttons[row][column] = btn

new_game()
window.mainloop()
