import os
import pygame, sys
from pygame.locals import *
from printrun.printcore import printcore
from printrun import gcoder
import xmlrpc.client
import time

# rpc = xmlrpc.client.ServerProxy('http://localhost:7978')
p = printcore('COM3', 115200)
gcode = []
pygame.init()
pygame.font.init()
background = (30, 30, 30)
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()
print("Width of screen:", w, "::", "Height of screen:", h)
mainLoop = True
current_state = [0]
printcount = 0

def display_loading():
    text_wait.visible = True
    text_wait.draw(DISPLAYSURF)
    time.sleep(2)
    text_wait.clear()
    
def is_printing():
    return p.printing or p.paused

def get_state():
    if not is_printing:
        return 0
    elif p.printing:
        return 1
    elif p.paused:
        return 2

def connect_printer():
    global p
    p = printcore('COM3', 115200)

def begin_print(fname):
    global gcode, current_state, printcount
    printcount += 1
    current_state[0] = 1
    gcode = [i.strip() for i in open(fname)]
    gcode = gcoder.LightGCode(gcode)
    p.startprint(gcode)
    print("PRINTING", fname)

def pause_print():
    p.pause()
    current_state[0] = 2
    while p.printing:
        display_loading()

def resume_print():
    p.resume()
    current_state[0] = 1

def disconnect_printer():
    p.disconnect()
    connect_printer()
    current_state[0] = 0

class ImageButton():
    def __init__(self, x, y, image, imageselected, scale = 1, onclick = (lambda x: 0), visibleon = [0]):
        self.x = x
        self.y = y
        self.scale = scale
        self.image = image
        self.imageselected = imageselected
        self.img = image
        self.imgrect = self.img.get_rect()
        self.visible = False
        self.visibleon = visibleon
        self.onclick = onclick
        self.update_image(image)
    
    def update_image(self, img):
        self.img = img
        self.img = pygame.transform.rotozoom(self.img, 0, self.scale)
        self.imgrect = img.get_rect()
        self.imgrect.left = self.x
        self.imgrect.top = self.y
        self.imgrect.width = self.imgrect.width
        self.imgrect.height = self.imgrect.height

    def handle_event(self, event):
    #     if event.__dict__['printing']:
    #         self.visible = False
    #     elif event.__dict__['selection']:
    #         self.visible = True
        if self.visible and event.type == pygame.MOUSEBUTTONUP and self.imgrect.collidepoint(pygame.mouse.get_pos()):
            self.onclick()

    def update(self):
        if not (self.visible == (current_state[0] in self.visibleon)):
            self.visible = not self.visible
            DISPLAYSURF.fill(pygame.Color("black"))
        if self.visible:
            if self.imgrect.collidepoint(pygame.mouse.get_pos()):
                self.update_image(self.imageselected)
            else:
                self.update_image(self.image)
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.img, self.imgrect)

class TextOut:
    def __init__(self, x, y, text, color = COLOR_ACTIVE, visibleon = []):
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.txt_surface_clear = FONT.render(text, True, background)
        self.visible = False
        self.visibleon = visibleon
    
    def handle_event(self, event):
        pass
    
    def update(self):
        if not (self.visible == (current_state[0] in self.visibleon)):
            self.visible = not self.visible
            DISPLAYSURF.fill(pygame.Color("black"))
    
    def clear(self):
        DISPLAYSURF.blit(self.txt_surface_clear, (self.x, self.y))

    def draw(self, screen):
        if self.visible:
            screen.blit(self.txt_surface, (self.x, self.y))

text_select = TextOut(w/2, h/5, "Select a print:", visibleon=[0])
text_refill = TextOut(w/3, h/5, "Please ask staff to refill the printer.", visibleon=[3])
text_printing = TextOut(w/2, h/5, "Printing:", visibleon=[1])
text_paused = TextOut(w/2, h/5, "Paused.", visibleon=[2])
text_wait = TextOut(w/2, h/4, "PLEASE WAIT...")
shape_triangle = ImageButton(w/2 - 300 - 150, h/2 - 150, pygame.image.load("images/" + "triangle.png"), pygame.image.load("images/" + "triangleselected.png"), 1, lambda: begin_print('printfiles/trianglehandcraft.gcode'), [0]) 
shape_circle = ImageButton(w/2 - 0   - 150, h/2 - 150, pygame.image.load("images/" + "circle.png"), pygame.image.load("images/" + "circleselected.png"), 1, lambda: begin_print('printfiles/circlehandcraft.gcode'), [0]) 
shape_square = ImageButton(w/2 + 300 - 150, h/2 - 150, pygame.image.load("images/" + "square.png"), pygame.image.load("images/" + "squareselected.png"), 1, lambda: begin_print('printfiles/squarehandcraft.gcode'), [0]) 
shape_play = ImageButton(w/2 - 300 - 150, h/2 - 150, pygame.image.load("images/" + "play.png"), pygame.image.load("images/" + "playselected.png"), 1, lambda: resume_print(), [2]) 
shape_pause = ImageButton(w/2 - 0   - 150, h/2 - 150, pygame.image.load("images/" + "pause.png"), pygame.image.load("images/" + "pauseselected.png"), 1, lambda: pause_print(), [1]) 
shape_stop = ImageButton(w/2 + 300 - 150, h/2 - 150, pygame.image.load("images/" + "stop.png"), pygame.image.load("images/" + "stopselected.png"), 1, lambda: disconnect_printer(), [1, 2]) 
items = [text_select, text_printing, text_paused, text_refill, shape_triangle, shape_circle, shape_square, shape_play, shape_pause, shape_stop]
while mainLoop:
    # if get_state():
    #     current_state[0] = get_state()
    # else:
    #     current_state[0] = 0
    if printcount >= 10:
        current_state[0] = 3
    for item in items:
        item.update()
        item.draw(DISPLAYSURF)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mainLoop = False
        # print(current_state)
        if event.type == pygame.QUIT:
            mainLoop = False
        for item in items:
            item.handle_event(event)
            item.update()
            item.draw(DISPLAYSURF)
        
    pygame.display.update()

p.disconnect()
pygame.quit()