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

    state = 'main_menu'
    learn_substate = 'grid'
    current_chapter = 1

    while True:
        mouse_pos = pygame.mouse.get_pos()

        if state == 'main_menu':
            menumod.draw_main_menu(surface, mouse_pos, SCALE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    action = menumod.hit_test(event.pos, SCALE, is_main_menu=True)
                    if action == "jogar":
                        state = 'chapter_select'
                    elif action == "aprender":
                        state = 'learn'
                        learn_substate = 'grid'

        elif state == 'learn':
            action = learnmod.draw(surface, learn_substate, mouse_pos, SCALE)
            if action == "voltar":
                state = 'main_menu'
            elif action == "voltar_lista":
                learn_substate = 'grid'
            elif isinstance(action, int) and 0 <= action < len(learnmod.TOPICS_DATA):
                learn_substate = action
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

        elif state == 'chapter_select':
            save_data = savemod.load()
            menumod.draw_chapter_select(surface, save_data, mouse_pos, SCALE)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = 'main_menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    chapter = menumod.hit_test(event.pos, SCALE, is_main_menu=False)
                    unlocked = chapter == 1 or (
                        chapter is not None and (chapter - 1) in save_data['chapters_completed'])
                    if chapter is not None and unlocked and gamemod.has_phases(chapter):
                        current_chapter = chapter
                        state = 'game'

        elif state == 'game':
            result = gamemod.play(window, surface, clock, current_chapter)
            if result == 'quit':
                pygame.quit()
                sys.exit()
            state = 'chapter_select'

        scaled = pygame.transform.scale(surface, (WINDOW_W, WINDOW_H))
        window.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()