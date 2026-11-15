import pygame
import sys
from config import *
import menu as menumod
import game as gamemod
import save as savemod

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Function Archer")
    clock = pygame.time.Clock()
    surface = pygame.Surface((INTERNAL_W, INTERNAL_H))
    state = 'menu'

    while True:
        if state == 'menu':
            save_data = savemod.load()
            menumod.draw(surface, save_data)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chapter = menumod.hit_test(event.pos, SCALE)
                    if chapter == 1: # Só deixa entrar no cap 1 por enquanto
                        state = 'game'
            clock.tick(FPS)
        elif state == 'game':
            result = gamemod.play(window, surface, clock, 1)
            if result == 'quit':
                pygame.quit(); sys.exit()
            state = 'menu'

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()

if __name__ == '__main__':
    main()