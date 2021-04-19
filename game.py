import tkinter as tk
from numpy import rot90
from copy import copy
from time import perf_counter


root = tk.Tk()
root.title('Tic Tac Toe')


player = ('X', 'O')
player_idx = 0
square_state = None


buttons = []

for i in range(9):
    b = tk.Button(root, text = ' ', font = ('Arial', 25), height = 12, width = 24, command = lambda i = i: make_move_if_valid(i))
    buttons.append(b)

for i in range(len(buttons)):
    buttons[i].grid(row = int(i / 3) + 1, column = i % 3)


def make_move_if_valid(button_idx):
    global player_idx
    global square_state
    if check_for_result(buttons) == None:
        if buttons[button_idx]['text'] != 'Invalid Move!':
            if buttons[button_idx]['text'] == ' ':
                buttons[button_idx]['text'] = player[player_idx]
                player_idx = (player_idx + 1) % 2 

                if check_for_result(buttons) != None:
                    print(check_for_result(buttons))
                    win_alert = tk.Label(root, text = check_for_result(buttons), font = ('Arial', 50))
                    win_alert.grid(row = 0, column = 1)

            else:
                square_state = buttons[button_idx]['text']
                buttons[button_idx]['text'] = 'Invalid Move!'
                root.after(750, lambda: buttons[button_idx].config(text = square_state))

        else:
            buttons[button_idx]['text'] = square_state


def check_for_result(buttons, from_minimax = False):
    for i in range(5):
        board_state = []

        for j in range(3):
            board_state.append([])
            for k in range(3):
                board_state[j].append(buttons[3 * j + k])

        #print(board_state)
        board_state = rot90(board_state, i)
        #print('after rot ' + str(i) + ': ' + str(board_state))

        if not from_minimax:
            if board_state[0][0]['text'] == board_state[0][1]['text'] == board_state[0][2]['text'] and board_state[0][0]['text'] != ' ':
                return board_state[0][0]['text'] + ' Wins!'

            elif board_state[0][1]['text'] == board_state[1][1]['text'] == board_state[2][1]['text'] and board_state[0][1]['text'] != ' ':
                return board_state[0][1]['text'] + ' Wins!'

            elif board_state[0][0]['text'] == board_state[1][1]['text'] == board_state[2][2]['text'] and board_state[0][0]['text'] != ' ':
                return board_state[0][0]['text'] + ' Wins!'

            for i in range(3):
                for j in range(3):
                    if board_state[i][j]['text'] == ' ':
                        return None

        else:
            if board_state[0][0] == board_state[0][1] == board_state[0][2] and board_state[0][0] != ' ':
                return board_state[0][0] + ' Wins!'

            elif board_state[0][1] == board_state[1][1] == board_state[2][1] and board_state[0][1] != ' ':
                return board_state[0][1] + ' Wins!'

            elif board_state[0][0] == board_state[1][1] == board_state[2][2] and board_state[0][0] != ' ':
                return board_state[0][0] + ' Wins!'

            for i in range(3):
                for j in range(3):
                    if board_state[i][j] == ' ':
                        return None
    
        return 'Tie!'


def minimax(board_state, depth, initial_depth, computer_to_move):
    # 1000 is used in lieu of infinity and -1000 is used in lieu of -infinity
    if depth == initial_depth:
        board_state_from_buttons = []
        for i in range(len(board_state)):
            board_state_from_buttons.append(board_state[i]['text'])

        board_state = board_state_from_buttons

    print(board_state)
    if depth == 0 or check_for_result(board_state, True) != None:
        print('End State Reached!')
        if check_for_result(buttons, True) == 'X Wins!':
            return [-1000 - depth + initial_depth]

        if check_for_result(board_state, True) == 'O Wins!':
            return [1000 + depth - initial_depth]

        if check_for_result(board_state, True) == 'Tie!':
            return [0]

        else:
            return [0]

    if computer_to_move:
        #print('c')
        for i in range(3):
            for j in range(3):
                if board_state[3 * i + j] == ' ':
                    board_state[3 * i + j] = 'O'
                    eval = minimax(board_state, depth - 1, initial_depth, False)
                    #print(eval)
                    max_eval = max(eval)
        
                    board_state[3 * i + j] = ' '
        
        return [max_eval]

    else:
        #print('p')
        for i in range(3):
            for j in range(3):
                if board_state[3 * i + j] == ' ':
                    board_state[3 * i + j] = 'X'
                    eval = minimax(board_state, depth - 1, initial_depth, True)
                    #print(eval)
                    min_eval = min(eval)
        
                    board_state[3 * i + j] = ' '
        
        return [min_eval]

print(minimax(buttons, 3, 3, True))
root.mainloop()

