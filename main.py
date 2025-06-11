import pygame

pygame.init()

from utils import WIDTH, WINDOW, FPS, clock, title_font
from menus import get_menu

def main():
    state = {
        "running": True,
        "current_menu": "main"
    }

    # Get initial menu
    current_buttons = get_menu("main")

    while state["running"]:
        mouse_pos = pygame.mouse.get_pos()
        WINDOW.fill("black")
        title = state["current_menu"].capitalize()
        title_text = title_font.render(title, True, "white")
        WINDOW.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

        for button in current_buttons:
            button.draw(WINDOW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state["running"] = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in current_buttons:
                    if button.is_clicked(mouse_pos):
                        next_menu = button.action()
                        if next_menu:
                            state["current_menu"] = next_menu
                            current_buttons = get_menu(next_menu)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
