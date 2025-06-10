from menu_button import MenuButton

import pygame
pygame.init()


WIDTH, HEIGHT = 1280, 720
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")
FPS = 60
clock = pygame.time.Clock()
clock.tick(FPS)
font_chess = pygame.font.SysFont(None, 100)

font = pygame.font.SysFont(None, 30)
buttons_name = ["Play", "Statistics", "Options", "Quit"]
buttons = []
for button_name in buttons_name:
    btn = MenuButton(WIDTH, HEIGHT, font, button_name)
    buttons.append(btn)
    
    
def draw_chess_text():
    text = font_chess.render("Chess", True, "white")
    WINDOW.blit(text, (WIDTH/2 - text.get_width()/2, 150))    
    
def main():
    
    run_menu = True 
    while run_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
                
        WINDOW.fill("black")
        draw_chess_text()
        for button in buttons:
            button.draw(WINDOW)   
        pygame.display.update()
	
    pygame.quit()
    
#only when we import the module, we want to execute the code and not directly when we compile
if __name__ == "__main__":
   main()