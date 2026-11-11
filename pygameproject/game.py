import pygame
import importlib
import os



os.chdir(os.path.dirname(os.path.abspath(__file__)))
pygame.init()

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)



screen = pygame.display.set_mode((2100, 1200))
clock = pygame.time.Clock()
FPS = 60
moving_left = False
moving_right = False
running = True
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2)

font = pygame.font.Font('freesansbold.ttf', 12)

def load_plugin(uppercase):
        module = importlib.import_module(f"plugins.{uppercase}")
        return module.apply

controls_file = 'gametext/controls.txt'

def get_game_text():
        with open(controls_file, encoding="utf-8") as f:
            text = load_plugin("uppercase")(f.read())
        return text

    
game_text = get_game_text()
render_text = font.render(game_text, True, white)
text_rect = render_text.get_rect()
text_rect.topleft = (10, 10)

class Soldier(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type   
        self.speed = speed
        self.direction = 1
        self.flip = False
        img = pygame.image.load(f'{self.char_type}/player_character_idle.png')
        self.img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = self.img.get_rect()
        self.rect.center = (x, y)
    def move(self, moving_left, moving_right):
        dx = 0
        dy = 0

        if moving_left:
             dx= -self.speed
             self.flip = True
             self.direction = -1

        if moving_right:
             dx= self.speed
             self.flip = False
             self.direction = 1

        self.rect.x += dx
        self.rect.y += dy



    def draw(self):
        screen.blit(pygame.transform.flip(self.img, self.flip, False), self.rect)

player = Soldier('player', 200, 200, 3, 5)




while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    screen.fill("blue")
    player.draw()
    player.move(moving_left, moving_right)
    screen.blit(render_text, text_rect)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
         running = False
    if keys[pygame.K_a]:
        moving_left = True
    else:
        moving_left = False
    if keys[pygame.K_d]:
        moving_right = True
    else:
        moving_right = False

    
    pygame.display.update()

    

pygame.quit()