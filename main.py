import gui

class Main():
    def __init__(self):
        self.gui = gui.GUI()
    def run(self):
        running = True
        self.gui.start()
        
        while running:
            inp = input("debug commands: ")
            if inp == 'e':
                self.gui.exit()
                self.gui.join()  
                running = False      
    
    
main = Main()
main.run()