import pygame

from constants import BG_COLOR, HEIGHT, WIDTH
from constants.menus import ScenesEnum
from ui.scene import Scene

class SceneManager:
    def __init__(self):
        self.running = True
        self.is_f11_clicked = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Chess")
        self.screen.fill(BG_COLOR)
        self.fullscreen_size = pygame.display.get_desktop_sizes()[0]

    def set_scene(self, scene: ScenesEnum):
        self.scene = Scene(self, scene)
        
    def quit(self):
        self.running = False

    def run_frame(self):
        dt = pygame.time.Clock().tick(144)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self.toggle_fullscreen()
            else:
                self.scene.handle_event(event)
        self.draw_scene()
        
    def toggle_fullscreen(self):
        self.is_f11_clicked = not self.is_f11_clicked
        if self.is_f11_clicked:
            self.screen = pygame.display.set_mode((self.fullscreen_size[0], self.fullscreen_size[1]), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            
    def draw_scene(self):
        self.screen.fill(BG_COLOR)
        self.scene.update()
        self.scene.render()
        pygame.display.flip()