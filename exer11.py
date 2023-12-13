from kivy.lang import Builder
from kivymd.app import MDApp

# define current player
game_ends = False
winner = ""
move_count = 0

########## MINIMAX ALGORITHM ##########
#initialize board configuration
CELLS_COUNT = 9
board_configuration = [] # contains the value of each cell
for i in range(CELLS_COUNT):
    board_configuration.append("")

# checks if state is terminal (i.e. final state)
def terminal(s):
    terminal = False
    # start checking only when there's three moves or more
    if move_count > 2:
        # check if a row of x or o has been formed

        # check if the board is filled
        terminal = True
        for i in range(CELLS_COUNT):
            if not board_configuration[i]:
                terminal = False
                break
        return terminal

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
        self.current_player = btn.text
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
        game_ends = terminal(board_configuration)
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