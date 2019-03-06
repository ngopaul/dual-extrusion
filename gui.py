import pygame, sys
from pygame.locals import *
from Printrun.printrun.printcore import printcore
from Printrun.printrun import gcoder
import xmlrpc.client

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
mainLoop = True
printing = 0

def is_printing():
    return p.printing or p.paused

def connect_printer():
    nonlocal p
    p = printcore('COM3', 115200)

def begin_print(fname):
    nonlocal gcode
    gcode = [i.strip() for i in open(fname)]
    gcode = gcoder.LightGCode(gcode)
    p.startprint(gcode)

def pause_print():
    p.pause()

def resume_print():
    p.resume()

def disconnect_printer():
    p.disconnect()

class ImageButton():
    def __init__(self, x, y, image, imageselected, scale = 1):
        self.x = x
        self.y = y
        self.scale = scale
        self.image = image
        self.imageselected = imageselected
        self.img = image
        self.imgrect = self.img.get_rect()
        self.visible = True

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
        if event.__dict__['printing']:
            self.visible = False
        elif event.__dict__['selection']:
            self.visible = True

    def update(self):
        if self.imgrect.collidepoint(pygame.mouse.get_pos()):
            self.update_image(self.imageselected)
        else:
            self.update_image(self.image)
    
    def draw(self, screen):
        if self.visible:
            screen.blit(self.img, self.imgrect)

class TextOut:
    def __init__(self, x, y, text, color = COLOR_ACTIVE):
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.txt_surface_clear = FONT.render(text, True, background)
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def clear(self):
        DISPLAYSURF.blit(self.txt_surface_clear, (self.x, self.y))

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.x, self.y))
    
shape1 = ImageButton(50, 50, pygame.image.load("images/" + "triangle.png"), pygame.image.load("images/" + "triangleselected.png")) 
shape2 = ImageButton(350, 50, pygame.image.load("images/" + "circle.png"), pygame.image.load("images/" + "circleselected.png")) 
shape3 = ImageButton(650, 50, pygame.image.load("images/" + "square.png"), pygame.image.load("images/" + "squareselected.png")) 
shapes = [shape1, shape2, shape3]
while mainLoop:
    for shape in shapes:
        shape.update()
        shape.draw(DISPLAYSURF)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
    pygame.display.update()

pygame.quit()