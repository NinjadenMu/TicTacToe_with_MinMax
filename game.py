import tkinter as tk
from numpy import rot90
import webbrowser


player = ('X', 'O')
player_idx = 0
square_state = None
win_alert = None
moves = 0


def make_move_if_valid(button_idx):
    global player_idx
    global square_state
    global win_alert
    global moves

    board_state = board_state_from_buttons()

    if check_for_result(board_state) == None:
        if buttons[button_idx]['text'] != 'Invalid Move!':
            moves += 1
            if buttons[button_idx]['text'] == ' ':
                buttons[button_idx]['text'] = player[player_idx]
                player_idx = (player_idx + 1) % 2 
                
                board_state = board_state_from_buttons()

                if check_for_result(board_state) != None:
                    #(check_for_result(board_state))
                    win_alert = tk.Label(root, text = check_for_result(board_state) + ' in ' + str(moves) + ' moves!', font = ('Arial', 50))
                    win_alert.grid(row = 0, column = 1)

            else:
                square_state = buttons[button_idx]['text']
                buttons[button_idx]['text'] = 'Invalid Move!'
                root.after(750, lambda: buttons[button_idx].config(text = square_state))

        else:
            buttons[button_idx]['text'] = square_state


def board_state_from_buttons():
    board_state = []
    for i in range(3):
        board_state.append([])
        for j in range(3):
            board_state[i].append(buttons[3 * i + j]['text'])

    return board_state


def check_for_result(board_state):
    for i in range(5):
        board_state = rot90(board_state, i)
        if board_state[0][0] == board_state[0][1] == board_state[0][2] and board_state[0][0] != ' ':
            return board_state[0][0] + ' Won'

        elif board_state[0][1] == board_state[1][1] == board_state[2][1] and board_state[0][1] != ' ':
            return board_state[0][1] + ' Won'

        elif board_state[0][0] == board_state[1][1] == board_state[2][2] and board_state[0][0] != ' ':
            return board_state[0][0] + ' Won'


    for i in range(3):
        for j in range(3):
            if board_state[i][j] == ' ':
                return None

    return 'Tie'


def minimax(board_state, player_idx, depth_limit, alpha, beta, depth = 0):
    if check_for_result(board_state) != None or depth == depth_limit:
        if check_for_result(board_state) == 'X Won':
            return 10 - depth

        elif check_for_result(board_state) == 'O Won':
            return -10 + depth

        else:
            return 0

    if player_idx == 0:
        move_scores = [-100 for i in range(9)]
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == ' ':
                    board_state[i][j] = 'X'
                    eval = minimax(board_state, (player_idx + 1) % 2, depth_limit, alpha, beta, depth + 1)
                    move_scores[3 * i + j] = eval
                    board_state[i][j] = ' '
                    
                    alpha = max(alpha, eval)
                    if alpha >= beta:
                        break
        
        if depth != 0:
            return max(move_scores)

        else:
            return move_scores.index(max(move_scores))

    else:
        move_scores = [100 for i in range(9)]
        for i in range(3):
            for j in range(3):
                if board_state[i][j] == ' ':
                    board_state[i][j] = 'O'
                    eval = minimax(board_state, (player_idx + 1) % 2, depth_limit, alpha, beta, depth + 1)
                    move_scores[3 * i + j] = eval
                    board_state[i][j] = ' '
                    
                    beta = min(beta, eval)
                    if alpha >= beta:
                        break

        if depth != 0:
            return min(move_scores)

        else:
            #print(move_scores)
            #print(player_idx)
            return move_scores.index(min(move_scores))


def make_computer_move():
    #print(moves)
    if moves == 0:
        make_move_if_valid(0)

    else:
        idx = minimax(board_state_from_buttons(), player_idx, 20, -100, 100)
        #print(idx)
        make_move_if_valid(idx)


def new_match():
    global player_idx
    global square_state
    global win_alert
    global moves

    for button in buttons:
        button['text'] = ' '

    player_idx = 0
    square_state = None
    moves = 0

    if win_alert != None:
        win_alert.destroy()
        win_alert = None


root = tk.Tk()
root.title('Tic Tac Toe')


buttons = []

for i in range(9):
    b = tk.Button(root, text = ' ', font = ('Arial', 25), height = 12, width = 24, command = lambda i = i: make_move_if_valid(i))
    buttons.append(b)

for i in range(len(buttons)):
    buttons[i].grid(row = int(i / 3) + 1, column = i % 3)

computer_move_button = tk.Button(root, text = 'Computer Move', command = make_computer_move)
computer_move_button.grid(row = 4, column = 0)

new_match_button = tk.Button(root, text = 'New Match', command = new_match)
new_match_button.grid(row = 4, column = 1)

view_source_code_button = tk.Button(root, text = 'Source Code', command = lambda: webbrowser.open('https://github.com/NinjadenMu/TicTacToe_with_MinMax'))
view_source_code_button.grid(row = 4, column = 2)


root.mainloop()