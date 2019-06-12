import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        super().__init__()
        self.screen=screen
        self.ai_settings=ai_settings


        self.image=pygame.image.load('images/alien.bmp')
        self.rect=self.image.get_rect()


        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        self.x=float(self.rect.x)

    def update(self):#重写
        self.x+=self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction
        self.rect.x=self.x


    def check_edges(self):
        screen_rect=self.screen.get_rect()
        if self.rect.right>=screen_rect.right:
            return True
        elif self.rect.left<=0:
            return True

    def blitme(self):
        '''在这里，只能估计传递的screen是引用传递'''
        self.screen.blit(self.image,self.rect)#只要创建一个新的可变对象，python就会分配一个新的地址
                                              # 在python中，不可变对象是共享的，创建可变对象永远是分配新地址
                                              #python有着自己的一套特殊的传参方式，这是由python动态语言的性质所决定的