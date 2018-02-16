import pygame
from pygame.locals import * 

import threading

class GUI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        pygame.init()
        display_info = pygame.display.Info()
     #   self.screen = pygame.display.set_mode((display_info.current_w, display_info.current_h),pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((800, 600)) 
        pygame.display.set_caption('Smart Mirror')
        self.screen.fill((240, 240 ,240))
        pygame.mouse.set_visible(False)
        self.running = True
    def run(self):
        font = pygame.font.Font('/usr/share/fonts/truetype/freefont/FreeSans.ttf',100)
        textsurface = font.render('Test', True, (255,0,0))     
        
        while self.running:
        #    for event in pygame.event.get():
        #        if (event.type == QUIT) or (event.type == pygame.KEYDOWN):
        #            running = False
            self.screen.blit(textsurface, (200,200))
            pygame.display.update()
        pygame.quit()  
    def exit(self):
        self.running = False
