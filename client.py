import tkinter.filedialog
import pygame
import sys
import requests
from cryptography.fernet import Fernet
import resource
import pickle
import hashlib

resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
sys.setrecursionlimit(100000)
pygame.init()
display = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Restore;")

def prompt_file():
    top = tkinter.Tk()
    top.withdraw() 
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
        self.download_url = ""

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
download_button = Button(400, 375, 130, 20, "Download")

download_key = ""
download_filename = ""

f = "<No File Selected>"

download_keys = []

is_on_download_page = False
download_buttons = []
try:
    download_keys = pickle.load(open("save.pickle", "rb"))
except:
    download_keys = []
while True:
    display.fill(pygame.color.Color("grey"))
    mx, my = pygame.mouse.get_pos()

    display.blit(text, textRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pickle.dump(download_keys, open("save.pickle", "wb"))
            pygame.quit()
            sys.exit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if select_file_button.rect.collidepoint((mx, my)):
                    f = prompt_file()
                if upload_button.rect.collidepoint((mx, my)):
                    if not is_on_download_page:
                        key = Fernet.generate_key()
                        _key = Fernet(key)
                        encrypted = _key.encrypt(open(f, "rb").read())
                        hash_encrypted = hashlib.sha256(encrypted).hexdigest()
                        print(hash_encrypted)
                        download_key = key.decode()
                        download_filename = f.split('/')[-1]
                        data = requests.post(f"http://127.0.0.1:5000/upload/{download_filename}", files={"file": encrypted}).json()
                        download_keys.append(f"http://127.0.0.1:5000/download/{hash_encrypted}/{download_filename}/{download_key}")
                if download_button.rect.collidepoint((mx, my)):
                    is_on_download_page = True


                for button in download_buttons:
                    if button.rect.collidepoint((mx, my)):
                        print(button.download_url.split("/")[-1])
                        data = requests.get(button.download_url)
                        with open(button.download_url.split("/")[-2], "wb") as file:    
                            f = Fernet(button.download_url.split("/")[-1])
                            file.write(f.decrypt(data.content))
    download_buttons = []

    if not is_on_download_page:
        select_file_button.draw(display, mx, my)
        upload_button.draw(display, mx, my)
        download_button.draw(display, mx, my)

        selected_file = font_small.render(f, True, (0,0,0))
        selected_file_rect = selected_file.get_rect()
        selected_file_rect.center = (800 // 2, 300)
        display.blit(selected_file, selected_file_rect)
    else:
        for index, key in enumerate(download_keys):
            button = Button(400, 200+index*4, 130, 20, key.split("/")[-2])
            button.download_url = key
            download_buttons.append(button)

    for download_button in download_buttons:
        download_button.draw(display, mx, my)

    pygame.display.update()
    clock.tick(60)
