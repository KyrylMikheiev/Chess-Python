import pygame

from scenes.menu_scene import MainMenuScene

class SceneManager:
    def __init__(self):
        self.current_scene = None
        self.running = True

    def change_scene(self, scene: MainMenuScene):
        self.current_scene = scene

    def quit(self):
        self.running = False

    def run_frame(self):
        dt = pygame.time.Clock().tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            else:
                self.current_scene.handle_event(event)

        self.current_scene.update(dt)
        self.current_scene.draw()
        pygame.display.flip()
