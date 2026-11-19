import pygame
import sqlite3
import datetime
import time
import importlib
import os
import argparse
import sys
import re
import io
from collections import Counter, defaultdict
from contextlib import redirect_stdout
from functools import lru_cache, partial, update_wrapper, wraps
from itertools import groupby, combinations
from collections.abc import Iterator

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

for folder in (BASE_DIR, PARENT_DIR):
    if folder not in sys.path:
        sys.path.insert(0, folder)

def build_parser():
     parser = argparse.ArgumentParser("Pytoolkit text untilities")
     sub = parser.add_subparsers(dest="command", required=True)

     analyze = sub.add_parser("analyze", help="Analyze a text file")
     analyze.add_argument("-f", "--file", required=True, help="Input file") 
     analyze.add_argument("-v", "--verbose", action="store_true")
     timer_parser = sub.add_parser('timer', help="Game timer")
     timer_parser.add_argument("-s", "--seconds", type=int, required=True, help="Game timer countup")
      


     return parser

def analyze_file(path, verbose=False):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    words = text.split()
    if verbose:
         print(f"Characters: {len(words)}")

def safe_read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{path}' not found.")
        return None

def load_plugin(uppercase):
        module = importlib.import_module(f"pygameproject.plugins.{uppercase}")
        return module.apply

def get_game_timer(seconds):
    start_time = time.monotonic()
    while True:
        elapsed = int(time.monotonic() - start_time)
        if elapsed >= seconds:
            print(seconds)
            break
        print(elapsed)
        time.sleep(1)

    

def run_game(seconds=0):
    pygame.init()
   
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 128)
    screen = pygame.display.set_mode((2100, 1200))
    clock = pygame.time.Clock()
    FPS = 60
    start_monotonic = time.monotonic()
    moving_left = False
    moving_right = False
    running = True
    player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() /2)
    font = pygame.font.Font('freesansbold.ttf', 12)
    controls_file = 'gametext/controls.txt'
    def get_game_text():
            with open(controls_file, encoding="utf-8") as f:
                text = load_plugin("uppercase")(f.read())
            return text

    def get_game_time():
        elapsed= int(time.monotonic() - start_monotonic) + seconds 
        return f"Time: {elapsed}s"




   
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
            img = pygame.image.load(f'{self.char_type}/idle/player_character_idle.png')
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
        timer_text = get_game_time()
        render_timer = font.render(timer_text, True, white)
        timer_rect = render_timer.get_rect()
        timer_rect.topleft = (10,35)
        screen.blit(render_timer, timer_rect)

       



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

def main():
    if len(sys.argv)>1:
        args = build_parser().parse_args()
        if args.command == "timer":
            run_game(seconds=args.seconds)
        if args.command == "analyze":
            text = safe_read(args.file)
            if text is None:
                sys.exit(1)

            analyze_file(args.file, args.verbose)
    else:
        run_game()
if __name__=="__main__":
     main()