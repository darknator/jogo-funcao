import pygame
import sys
from config import *
import menu as menumod
import game as gamemod
import learn as learnmod
import save as savemod


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Function Archer")
    clock = pygame.time.Clock()
    surface = pygame.Surface((INTERNAL_W, INTERNAL_H))

    state = 'main_menu'  # 'main_menu', 'learn', 'chapter_select', 'game'

    while True:
        mouse_pos = pygame.mouse.get_pos()

        if state == 'main_menu':
            menumod.draw_main_menu(surface, mouse_pos, SCALE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit();
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = menumod.hit_test(event.pos, SCALE, is_main_menu=True)
                    if action == "jogar":
                        state = 'chapter_select'
                    elif action == "aprender":
                        state = 'learn'

        elif state == 'learn':
            learnmod.draw(surface)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = 'main_menu'

        elif state == 'chapter_select':
            save_data = savemod.load()
            menumod.draw_chapter_select(surface, save_data, mouse_pos, SCALE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = 'main_menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chapter = menumod.hit_test(event.pos, SCALE, is_main_menu=False)
                    if chapter == 1:  # Só liberado o 1 por enquanto
                        state = 'game'

        elif state == 'game':
            result = gamemod.play(window, surface, clock, 1)
            if result == 'quit': pygame.quit(); sys.exit()
            state = 'chapter_select'  # Volta para a seleção de mundos

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()