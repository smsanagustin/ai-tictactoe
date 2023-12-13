from kivy.lang import Builder
from kivymd.app import MDApp

# define current player
game_ends = False
winner = ""
move_count = 0
player = ""

########## MINIMAX ALGORITHM ##########
#initialize board configuration
CELLS_COUNT = 9
board_configuration = [] # contains the value of each cell
for i in range(CELLS_COUNT):
    board_configuration.append("")

# checks if state is terminal (i.e. final state) and returns result
def terminal(state):
    utility = -1
    if move_count > 2:
        # check if first corner
        if state[0]:
            # row
            if state[0] == state[1] == state[2]: 
                if state[0] == player:
                    utility = 1
                return True, state[0], utility
            # diagonal
            elif state[0] == state[4] == state[8]:
                if state[0] == player:
                    utility = 1
                return True, state[0], utility
            # column
            elif state[0] == state[3] == state[6]:
                if state[0] == player:
                    utility = 1
                return True, state[0], utility
        # check second cell
        if state[1]:
            if state[1] == state[4] == state[7]:
                if state[1] == player:
                    utility = 1
                return True, state[1], utility
        # check last cell
        if state[2]:
            if state[2] == state[5] == state[8]:
                if state[2] == player:
                    utility = 1
                return True, state[2], utility
            elif state[2] == state[4] == state[6]:
                if state[2] == player:
                    utility = 1
                return True, state[2], utility
        if state[3]:
            if state[3] == state[4] == state[5]:
                if state[3] == player:
                    utility = 1
                return True, state[3], utility
        if state[6]:
            if state[6] == state[7] == state[8]:
                if state[6] == player:
                    utility = 1
                return True, state[6], utility

        # check if the board is filled
        for i in range(CELLS_COUNT):
            if not board_configuration[i]:
                return False, ""
        return True, "draw", 0
    return False, ""
   
# def max_value(state):
    
                
# graphical user interface
class MainApp (MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('board.kv')
    
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
        global player
        self.current_player = btn.text
        player = btn.text
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
    def end_game(self, btn):
        # disable buttons
        self.disable_buttons()
        
        # prompt user who won
        self.root.ids.label.text = f"{btn.text} wins!"
    
    # check if a player has won
    def check_win(self, btn):
        # iterate over the board to check if all cells are filled
        checker = terminal(board_configuration)
        print("checker", checker)
        game_ends = checker[0]
        result = checker[1]
        print(result)
        if game_ends:
            self.end_game(btn);
   
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
            print("move_count: ", move_count)
                
            print(board_configuration)
            
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
            print("move_count: ", move_count)
                
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
        self.turn = self.current_player # first turn always goes to the user
        
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
        prompt_text = self.current_player + " goes first."
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