import pygame

from utils.utils import BG_COLOR

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.running = True
        self.is_f11_clicked = True
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((1280, 1024), pygame.RESIZABLE)
        self.screen.fill(BG_COLOR)

    def change_scene(self, scene):
        self.current_scene = scene
        
    def quit(self):
        self.running = False

    def run_frame(self):
        dt = pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    if self.is_f11_clicked:
                        self.is_f11_clicked = False
                        pygame.display.set_mode((1280, 1024), pygame.RESIZABLE)
                    else:
                        self.is_f11_clicked = True
                        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                self.current_scene.handle_event(event)

        self.screen.fill(BG_COLOR)
        self.current_scene.update(self.screen)
        self.current_scene.render(self.screen)
        pygame.display.flip()
