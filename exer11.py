from kivy.lang import Builder
from kivymd.app import MDApp

class MainApp (MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('toe.kv')
    
    turn = "X" # x's turn
   
    # O or X will make a move 
    def presser(self, btn):
        if self.turn == 'X':
            btn.text = "X"
            btn.disabled = True
            self.root.ids.score.text = "O's turn!"
            
            # who will move next
            self.turn = "O"
            
        else:
            btn.text = "O"
            btn.disabled = True
            self.root.ids.score.text = "X's turn!"
            
            self.turn = "X"
    
    def restart(self):
        # reset turns
        self.turn = "X"
        
        # update player prompt
        self.root.ids.score.text = "X's turn"
        
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