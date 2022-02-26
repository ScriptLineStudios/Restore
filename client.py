import tkinter
import tkinter.filedialog
import pygame
import sys
import requests

pygame.init()
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Restore;")


def prompt_file():
    """Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = font_small.render(text, True, (0,0,0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (self.x, self.y)
        self.rect = pygame.Rect(self.x-self.width/2, self.y-self.height/2, self.width, self.height)

    def draw(self, display, mx, my):
        if self.rect.collidepoint((mx,my)):
            pygame.draw.rect(display, (120, 120, 120), self.rect)
            display.blit(self.text, self.textRect) 
        else:   
            pygame.draw.rect(display, (140, 140, 140), self.rect)
            display.blit(self.text, self.textRect)

font = pygame.font.Font('freesansbold.ttf', 48)
font_small = pygame.font.Font('freesansbold.ttf', 16)
text = font.render('Welcome', True, (0,0,0))
textRect = text.get_rect()
textRect.center = (800 // 2, 70)
select_file_button = Button(400, 325, 130, 20, "Select File")
upload_button = Button(400, 350, 130, 20, "Upload")

f = "<No File Selected>"
while True:
    display.fill(pygame.color.Color("grey"))
    mx, my = pygame.mouse.get_pos()

    display.blit(text, textRect)

    selected_file = font_small.render(f, True, (0,0,0))
    selected_file_rect = selected_file.get_rect()
    selected_file_rect.center = (800 // 2, 300)
    display.blit(selected_file, selected_file_rect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if select_file_button.rect.collidepoint((mx, my)):
                    f = prompt_file()
                if upload_button.rect.collidepoint((mx, my)):
                    data = requests.post("http://127.0.0.1:5000/upload", files={"file": open(f, "rb")}).json()
                    print(data)

    select_file_button.draw(display, mx, my)
    upload_button.draw(display, mx, my)

    pygame.display.update()
    clock.tick(60)
