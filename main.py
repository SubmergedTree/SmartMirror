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
        img_path = ''
        try:
            img_path = self.__find_img_dir()
        except OSError:
            running = False
            print("Error on __find_img_dir")    
        while running:
            inp = input("debug commands: ")
            if inp == 'e':
                self.gui.exit()
                self.gui.join()  
                running = False  
            if inp == 's':
                pass       
    def __find_img_dir(self):
        path = os.getcwd()
        path += '/img'
        try:
            os.makedirs(path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        return path
    
main = Main()
main.run()