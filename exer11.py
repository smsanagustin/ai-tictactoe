import random
from kivy.lang import Builder
from kivymd.app import MDApp

# define current player
game_ends = False
winner = ""
move_count = 0
user_player = ""

########## MINIMAX ALGORITHM ##########
#initialize board configuration
CELLS_COUNT = 9
board_configuration = [] # contains the value of each cell
for i in range(CELLS_COUNT):
    board_configuration.append("")
    
# checks if the board is empty
def board_empty(state):
    empty = True
    for i in range(CELLS_COUNT):
        if state[i]:
            empty = False 
            break
    return empty

# returns the player to move next given a state
def player(state):
    turn = "X"
    # if board is empty, return "X"
    if not board_empty(state):
        # if the counts of x and o are not equal, it's o's turn
        x_count = 0
        o_count = 0
        for i in range(CELLS_COUNT):
            if state[i] == "X":
                x_count += 1
            elif state[i] == "O":
                o_count += 1
        
        if not (x_count == o_count):
            turn = "O"
    
    return turn
    
# returns all possible moves of current player given a state
def actions(state):
    # check all possible configurations
    indices = []
    for i in range(CELLS_COUNT): # track empty cells
        if state[i] == "":
            indices.append(i)
    print(indices)
    return indices

# resulting state when action a is done on a state; action - index of the cell
def result(state, action):
    # check whose turn it is
    turn = player(state) 
    
    # create a state copy
    state_copy = []
    for i in range(CELLS_COUNT):
        state_copy.append(state[i]) 
    
    # add move to the current action
    state_copy[action] = turn
    return state_copy 

# returns 1 if X wins the game
# def utility(state):
    
# gets the winner of game
def winner(state):
    # check first if there is a winner
    winner = None
    if state[0]:
        # row
        if state[0] == state[1] == state[2]: 
            return state[0]
        # diagonal
        elif state[0] == state[4] == state[8]:
            return state[0]
        # column
        elif state[0] == state[3] == state[6]:
            return state[0]
    # check second cell
    if state[1]:
        if state[1] == state[4] == state[7]:
            return state[1]
    # check last cell
    if state[2]:
        if state[2] == state[5] == state[8]:
            return state[2]
        elif state[2] == state[4] == state[6]:
            return state[2]
    if state[3]:
        if state[3] == state[4] == state[5]:
            return state[3]
    if state[6]:
        if state[6] == state[7] == state[8]:
            return state[6]

    return winner

# returns the value of a state
def utility(state):
    # get the winner
    won = winner(state)
    if won == "X":
        return 1
    elif won == "O":
        return -1
    else:
        return 0
     
# checks if state is terminal (i.e. final state) and returns result
def terminal(state):
    board_filled = True
    # check first of all cells are filled
    for i in range(CELLS_COUNT):
        if not state[i]: # there's an empty cell
            board_filled = False
            break
        
    # if board is not filled, check if there's a winner
    if not board_filled:
        won = winner(state)
        if won is not None:
            return True
    return board_filled
    
def max_value(state):
    m = float('-inf')
    for action in actions(state):
        v = value(result(state, action))[0]
        if v > m:
            m = v
            move = action
    return m, move
    
def min_value(state):
    m = float('inf')
    for action in actions(state):
        v = value(result(state, action))[0]
        if v < m:
            m = v
            move = action
    return m, move

    

# return value of a state depending on who the player is
# 0th index - value; 1st index - move
def value(state):
    if terminal(state):
        return utility(state), None
    else:
        state_player = player(state)
        if state_player == "X": # max_node
            return max_value(state) # index 0 - value; index 1 - move
        else:
            return min_value(state)

# graphical user interface
class MainApp (MDApp):
    def build(self):
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('board.kv')
    
    first_player = "X"
    turn = ""
    current_player = ""
    buttons_list = []
    
    def save_buttons(self):
        self.buttons_list = [
        self.root.ids.btn1,
        self.root.ids.btn2,
        self.root.ids.btn3,
        self.root.ids.btn4,
        self.root.ids.btn5,
        self.root.ids.btn6,
        self.root.ids.btn7,
        self.root.ids.btn8,
        self.root.ids.btn9,
    ]

    
    def disable_options(self):
        self.root.ids.playerX.disabled = True
        self.root.ids.playerO.disabled = True
        
    def enable_options(self): 
        self.root.ids.playerX.disabled = False
        self.root.ids.playerO.disabled = False
    
    # set player based on which button the user clicks
    def setTurn(self, btn):
        global user_player
        self.current_player = btn.text
        user_player = btn.text
        self.turn = btn.text 
        self.disable_buttons()
        self.root.ids.play_button.text = "PLAY"
        self.root.ids.label.text = f"You are player {self.current_player}. Click PLAY to start!"
        self.root.ids.play_button.disabled = False
    
    # disable buttons
    def disable_buttons(self):
        self.root.ids.btn1.disabled = True
        self.root.ids.btn2.disabled = True
        self.root.ids.btn3.disabled = True
        self.root.ids.btn4.disabled = True
        self.root.ids.btn5.disabled = True
        self.root.ids.btn6.disabled = True
        self.root.ids.btn7.disabled = True
        self.root.ids.btn8.disabled = True
        self.root.ids.btn9.disabled = True
        
    def enable_buttons(self):
         # enable all buttons again
        self.root.ids.btn1.disabled = False
        self.root.ids.btn2.disabled = False
        self.root.ids.btn3.disabled = False
        self.root.ids.btn4.disabled = False
        self.root.ids.btn5.disabled = False
        self.root.ids.btn6.disabled = False
        self.root.ids.btn7.disabled = False
        self.root.ids.btn8.disabled = False
        self.root.ids.btn9.disabled = False
    
    # ends the game
    def end_game(self, result):
        # disable buttons
        self.disable_buttons()
        
        # prompt user who won
        if result not in ["X","O"]:
            self.root.ids.label.text = "DRAW!"
        else:
            if result == user_player:
                self.root.ids.label.text = "You win!"
            else:
                self.root.ids.label.text = "AI wins!"
    
    # check if a player has won
    def check_win(self, btn):
        # iterate over the board to check if all cells are filled
        if terminal(board_configuration):
            result = winner(board_configuration)
            self.end_game(result);
            
    # executes when AI moves
    def AI_presser(self, btn):
        self.disable_options()
        
        print("turn: ", self.turn);
        btn.text = self.turn
        btn.disabled = True
        self.root.ids.label.text = "Your turn!"
        
        # update board configuration (state)
        board_configuration[btn.index] = btn.text
        global move_count
        move_count += 1
            
            
        # who will move next
        if self.current_player == "X":
            self.turn = "X"
        else:
            self.turn = "O" 
            
        self.check_win(btn) # check first if a player has won 
            
    # executes when a button is clicked
    def presser(self, btn): 
        self.disable_options()
        
        if self.turn == self.current_player:
            btn.text = self.current_player
            btn.disabled = True
            self.root.ids.label.text = "AI is choosing a move..."
            
            # update board configuration (state)
            board_configuration[btn.index] = btn.text
            global move_count
            move_count += 1
             
            # who will move next
            if self.current_player == "X":
                self.turn = "O"
            else:
                self.turn = "X"
                
            
            self.check_win(btn) # check first if a player has won 
                 
            # find ai's turn based on the minimax algorithm
            ai_move = value(board_configuration)[1]
            print("next move:", str(ai_move))  
            
            # # finds button that corresponds to ai's chosen move
            for button in self.buttons_list:
                if button.index == ai_move:
                    self.AI_presser(button)
                    break 
                     
        # print(terminal(board_configuration))
        self.check_win(btn) # check first if a player has won 
             
    def start(self, play_button): 
        global move_count, ai_move
        # reset move count
        move_count = 0
        
        # save buttons
        self.save_buttons()
        
        # set turn
        self.turn = self.first_player # X always goes first
        
        # reset cells
        for i in range(len(board_configuration)):
            board_configuration[i] = ""
        
        # if player restarts, allow reselecting new player
        if play_button.text == "RESTART":
            self.enable_options()
        else:
            # disable picking player
            self.disable_options()
        
        # update player prompt
        if user_player == "X":
            prompt_text = self.first_player + " goes first."
            self.enable_buttons()
        else:
            prompt_text = "AI is choosing a move..."
            ai_move = random.randint(0, 9)

        self.root.ids.label.text = prompt_text
        play_button.text = "RESTART" 
                 
        # clear buttons
        self.root.ids.btn1.text = ""
        self.root.ids.btn2.text = ""
        self.root.ids.btn3.text = ""
        self.root.ids.btn4.text = ""
        self.root.ids.btn5.text = ""
        self.root.ids.btn6.text = ""
        self.root.ids.btn7.text = ""
        self.root.ids.btn8.text = ""
        self.root.ids.btn9.text = ""   
        
        # if it's ai's turn, let the ai move
        if user_player == "O":
            for button in self.buttons_list:
                if button.index == ai_move:
                    self.enable_buttons()
                    self.AI_presser(button)
                    break   
    
MainApp().run()

# Reference
# GUI: https://www.youtube.com/watch?v=PAnpsrEOQ4s
# KivyMD documentation: https://kivymd.readthedocs.io/en/1.1.1/getting-started/
# Minimax algorithm: https://youtu.be/WbzNRTTrX0g?list=PLhQjrBD2T381PopUTYtMSstgk-hsTGkVm&t=4327