import os
import errno

import gui
import database

class Main():
    def __init__(self):
        self.gui = gui.GUI()
    def run(self):
        with database.CreateDatabase() as db:
            db.create_database()
        running = True
        self.gui.start()
        try:
            self.__find_img_dir()
        except OSError:
            running = False
            print("Error on __find_img_dir")    
        while running:
            inp = input("debug commands: ")
            if inp == 'e':
                self.gui.exit()
                self.gui.join()  
                running = False     
    def __find_img_dir(self):
        try:
            os.makedirs("img")
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    
main = Main()
main.run()