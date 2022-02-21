#!/usr/bin/env python3

import pygame
from pygame.locals import *
import random
import sys



class Card:

    def __init__(self,value,x,y,z,is_showing):

        self.value=value
        self.x=x
        self.y=y
        self.z=z
        self.is_showing=is_showing

        self.destx=0
        self.desty=0
        self.is_moving=False

    def draw(self,display):
        if self.is_showing:
            display.blit(self.cards_img,(int(self.x),int(self.y)),self.cards_rect[self.value])
        else:
            display.blit(self.cards_img,(int(self.x),int(self.y)),self.cards_rect[CARD_BACK_VALUE])

    def update(self):

        slow=6
        epsilon=0.5

        if self.is_moving:

            diffx=self.destx-self.x
            diffy=self.desty-self.y

            self.x+=diffx/slow
            self.y+=diffy/slow
        
            if abs(diffx)<=epsilon:
                self.x=self.destx

            if abs(diffy)<=epsilon:
                self.y=self.desty

            if diffx==0 and diffy==0:
                self.is_moving=False            
   
    def move_to(self,x,y):
        self.destx=x
        self.desty=y
        self.is_moving=True




class Mouse:
    def __init__(self):
        self.x=0
        self.y=0
        self.button=0




def inrect(x,y,rx,ry,rw,rh):
    return x>=rx and x<=rx+rw and y>=ry and y<=ry+rh




FPS = 30

SCREEN_WIDTH=640
SCREEN_HEIGHT=640

BLACK = ( 22, 22, 22)
RED   = (171, 70, 70)
BLUE  = (143,155,246)
GREEN = (  0, 80,  0)
WHITE = (240,240,240)

MOUSE_BUTTON_LEFT=0
MOUSE_BUTTON_RIGHT=2


CARD_WIDTH=71
CARD_HEIGHT=96
CARD_BACK_VALUE=52

pygame.display.init()
clock = pygame.time.Clock()

display = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("PyTongIts")

mouse=Mouse()

cards_img = pygame.image.load("cards.png")
cards_img.set_colorkey((0,99,0),pygame.RLEACCEL)



cards_rect=[]
for i in range(0,53):
    cards_rect.append(((i%13)*CARD_WIDTH,int(i/13)*CARD_HEIGHT,CARD_WIDTH,CARD_HEIGHT))

Card.cards_img=cards_img
Card.cards_rect=cards_rect






pile=[]



values=[]
for i in range(0,52):
    values.append(i)
random.shuffle(values)


minz=0
maxz=0

cards=[]
entities=[]
for i in range(0,len(values)):
    card=Card(values[i],0,0,maxz,False)
    cards.append(card)
    entities.append(card)
    maxz+=1



stock=[]
for i in range(0,len(cards)):
    stock.append(cards[i])



hands=[]
for h in range(0,3):
    hands.append([])
    for c in range(0,13 if h==0 else 12):
        hands[h].append(stock.pop(len(stock)-1))
        hands[h][c].move_to(c*(CARD_WIDTH/4),h*(CARD_HEIGHT+CARD_HEIGHT/8)+CARD_HEIGHT+CARD_HEIGHT/8)



dt=0

dh=0
dc=0
is_dealing=True

diffx=0
diffy=0
is_dragging=False
drag_entity=None

mouse_right_hold=False

current_card=None

quit = False
while not quit:

    event=pygame.event.poll()

    if event.type == pygame.QUIT:
        quit = True
    elif event.type == pygame.MOUSEBUTTONDOWN:
        mouse.x,mouse.y=event.pos
    elif event.type == pygame.MOUSEBUTTONUP:
        mouse.x,mouse.y=event.pos
    elif event.type == pygame.MOUSEMOTION:
        mouse.x,mouse.y=event.pos
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            quit=True
        elif event.key == pygame.K_f:
            if event.mod == pygame.KMOD_NONE:     
                 if current_card != None:
                    current_card.z+=1
                    if current_card.z>maxz:
                        maxz=current_card.z+1  
            elif event.mod & pygame.KMOD_SHIFT:        
                if current_card != None:
                    current_card.z=maxz+1  
        elif event.key == pygame.K_b:
            if event.mod == pygame.KMOD_NONE:     
                 if current_card != None:
                    current_card.z-=1
                    if current_card.z<minz:
                        minz=current_card.z-1
            elif event.mod & pygame.KMOD_SHIFT:        
                if current_card != None:
                    current_card.z=minz-1
 

 
    mouse.button=pygame.mouse.get_pressed()


    display.fill(GREEN)


    entities.sort(key=lambda entity:entity.z,reverse=True)
    for i in range(len(entities)-1,-1,-1):
        entities[i].draw(display)




    if not is_dragging:
        if mouse.button[MOUSE_BUTTON_LEFT]:
            for i in range(len(entities)):
                entity=entities[i]
                if type(entity) is Card:
                    if inrect(mouse.x,mouse.y,entity.x,entity.y,CARD_WIDTH,CARD_HEIGHT):
                        maxz+=1
                        entity.z=maxz
                        diffx=entity.x-mouse.x
                        diffy=entity.y-mouse.y
                        drag_entity=entity
                        current_card=entity
                        is_dragging=True
                        break
    elif mouse.button[MOUSE_BUTTON_LEFT]:
        drag_entity.x=mouse.x+diffx
        drag_entity.y=mouse.y+diffy
        drag_entity.z=maxz+1
    else:
        is_dragging=False            



    if mouse.button[MOUSE_BUTTON_RIGHT]:
        if not mouse_right_hold:
            mouse_right_hold=True
            for i in range(len(entities)):
                entity=entities[i]
                if type(entity) is Card:
                    if inrect(mouse.x,mouse.y,entity.x,entity.y,CARD_WIDTH,CARD_HEIGHT):
                        entity.is_showing = not entity.is_showing
                        break
    else:
        mouse_right_hold=False



    if is_dealing:

        hands[dh][dc].z=maxz
        hands[dh][dc].update()
        if not hands[dh][dc].is_moving:

            hands[dh][dc].is_showing=True

            maxz+=1
            dc+=1
            if dc>=len(hands[dh]):
                dc=0
                dh+=1
                if dh>=len(hands):
                    is_dealing=False

    else:

        for h in range(0,len(hands)):
            for c in range(0,len(hands[h])):
                hands[h][c].update()



    pygame.display.flip()
    dt=clock.tick(FPS)/1000


pygame.quit()
sys.exit()
