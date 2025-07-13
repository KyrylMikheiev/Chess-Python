import pygame

from utils.utils import BG_COLOR, HEIGHT, WIDTH

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.running = True
        self.is_f11_clicked = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Chess")
        self.screen.fill(BG_COLOR)
        self.fullscreen_size = pygame.display.get_desktop_sizes()[0]

    def change_scene(self, scene):
        self.current_scene = scene
        
    def quit(self):
        self.running = False

    def run_frame(self):
        dt = pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self.toggle_fullscreen()
            else:
                self.current_scene.handle_event(event)

        self.screen.fill(BG_COLOR)
        self.current_scene.update(self.screen)
        self.current_scene.render(self.screen)
        pygame.display.flip()
        
    def toggle_fullscreen(self):
        self.is_f11_clicked = not self.is_f11_clicked
        if self.is_f11_clicked:
            self.screen = pygame.display.set_mode((self.fullscreen_size[0], self.fullscreen_size[1]), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)