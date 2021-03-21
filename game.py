import tkinter as tk
from numpy import rot90

root = tk.Tk()
root.title('Tic Tac Toe')


player = ('X', 'O')
player_idx = 0

buttons = []

for i in range(9):
    b = tk.Button(root, text = ' ', font = ('Arial', 25), height = 12, width = 24, command = lambda i = i: check_if_valid(i))
    buttons.append(b)

for i in range(len(buttons)):
    buttons[i].grid(row = int(i / 3) + 1, column = i % 3)
    #buttons[i].position = (int(i / 3), (i + 1) % 3)

def check_if_valid(button_idx):
    global player_idx

    if buttons[button_idx]['text'] == ' ':
        buttons[button_idx]['text'] = player[player_idx] 

        if check_for_result() != None:
            print(check_for_result())
            win_alert = tk.Label(root, text = check_for_result(), font = ('Arial', 50))
            win_alert.grid(row = 0, column = 1)

    else:
       square_state = buttons[button_idx]['text']
       buttons[button_idx]['text'] = 'Invalid Move!'
       root.after(750, lambda: buttons[button_idx].config(text = square_state))

    player_idx = (player_idx + 1) % 2

def check_for_result():
    for i in range(5):
        board_state = []

        for j in range(3):
            board_state.append([])
            for k in range(3):
                board_state[j].append(buttons[3 * j + k])

        #print(board_state)
        board_state = rot90(board_state, i)
        #print('after rot ' + str(i) + ': ' + str(board_state))

        if board_state[0][0]['text'] == board_state[0][1]['text'] == board_state[0][2]['text'] and board_state[0][0]['text'] != ' ':
            return board_state[0][0]['text'] + ' Wins!'

        elif board_state[0][1]['text'] == board_state[1][1]['text'] == board_state[2][1]['text'] and board_state[0][1]['text'] != ' ':
            return board_state[0][1]['text'] + ' Wins!'

        elif board_state[0][0]['text'] == board_state[1][1]['text'] == board_state[2][2]['text'] and board_state[0][0]['text'] != ' ':
            return board_state[0][0]['text'] + ' Wins!'

root.mainloop()

