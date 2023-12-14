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
    possible_moves = [] 
    
    # check first whose turn it is
    turn = player(state)
        
    # check all possible configurations
    indices = []
    for i in range(CELLS_COUNT): # track empty cells
        if state[i] == "":
            indices.append(i)
            
    # create a copy of the board configuration for each possible move
    for i in range(len(indices)):
        new_state = []
        for j in range(CELLS_COUNT):
            new_state.append(state[j])
        
        new_state[indices[i]] = turn
        possible_moves.append(new_state)
        
    return possible_moves
    
    
# checks if state is terminal (i.e. final state) and returns result
def terminal(state):
    utility = -1
    if move_count > 2:
        # check if first corner
        if state[0]:
            # row
            if state[0] == state[1] == state[2]: 
                if state[0] == user_player:
                    utility = 1
                return True, state[0], utility
            # diagonal
            elif state[0] == state[4] == state[8]:
                if state[0] == user_player:
                    utility = 1
                return True, state[0], utility
            # column
            elif state[0] == state[3] == state[6]:
                if state[0] == user_player:
                    utility = 1
                return True, state[0], utility
        # check second cell
        if state[1]:
            if state[1] == state[4] == state[7]:
                if state[1] == user_player:
                    utility = 1
                return True, state[1], utility
        # check last cell
        if state[2]:
            if state[2] == state[5] == state[8]:
                if state[2] == user_player:
                    utility = 1
                return True, state[2], utility
            elif state[2] == state[4] == state[6]:
                if state[2] == user_player:
                    utility = 1
                return True, state[2], utility
        if state[3]:
            if state[3] == state[4] == state[5]:
                if state[3] == user_player:
                    utility = 1
                return True, state[3], utility
        if state[6]:
            if state[6] == state[7] == state[8]:
                if state[6] == user_player:
                    utility = 1
                return True, state[6], utility

        # check if the board is filled
        for i in range(CELLS_COUNT):
            if not board_configuration[i]:
                return False, "", 0
        return True, "draw", 0
    return False, "", 0


   
def max_value(state):
    if terminal(state)[0]:
        return terminal(state)[2] # state utility is also returned by the terminal
    
                
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
    
    # ends the game
    def end_game(self, result):
        # disable buttons
        self.disable_buttons()
        
        # prompt user who won
        if result not in ["X","O"]:
            self.root.ids.label.text = "DRAW!"
        else:
            self.root.ids.label.text = f"{result} wins!"
    
    # check if a player has won
    def check_win(self, btn):
        # iterate over the board to check if all cells are filled
        checker = terminal(board_configuration)
        game_ends = checker[0]
        result = checker[1]
        utility = checker[2]
        print(result)
        if game_ends:
            print(utility)
            self.end_game(result);
   
    # executes when a button is clicked
    def presser(self, btn): 
        self.disable_options()
        
        if self.turn == self.current_player:
            btn.text = self.current_player
            btn.disabled = True
            self.root.ids.label.text = "AI's turn!"
            
            # update board configuration (state)
            board_configuration[btn.index] = btn.text
            global move_count
            move_count += 1
                
            print(board_configuration)
            print(actions(board_configuration))
            
            # who will move next
            if self.current_player == "X":
                self.turn = "O"
            else:
                self.turn = "X"
        
        # ai's turn
        else:
            if self.current_player == "X":
                btn.text = "O"
            else:
                btn.text = "X" 
                
            btn.disabled = True
            self.root.ids.label.text = "Your turn!"

            # update board configuration (state)
            board_configuration[btn.index] = btn.text
            move_count += 1
                
            print(board_configuration)
             
            if self.current_player == "X":
                self.turn = "X"
            else:
                self.turn = "O"
             
        self.check_win(btn) # check first if a player has won
    
    def start(self, play_button): 
        global move_count
        # reset move count
        move_count = 0
        
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
        prompt_text = self.first_player + " goes first."
        self.root.ids.label.text = prompt_text
        play_button.text = "RESTART"
        
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
    
MainApp().run()

# Reference
# GUI: https://www.youtube.com/watch?v=PAnpsrEOQ4s
# KivyMD documentation: https://kivymd.readthedocs.io/en/1.1.1/getting-started/
# Minimax algorithm: https://youtu.be/WbzNRTTrX0g?list=PLhQjrBD2T381PopUTYtMSstgk-hsTGkVm&t=4327