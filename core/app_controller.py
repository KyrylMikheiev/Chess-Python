from core.scene_manager import SceneManager
from core.scenes_enum import ScenesEnum

class AppController:
    
    def __init__(self):
        self.scene_manager = SceneManager()
        self.scene_manager.set_scene(ScenesEnum.MAIN_MENU)
        while self.scene_manager.running:
            self.scene_manager.run_frame()

    """
        - We have a list of menus
        - Each menu has buttons
        - When a button is clicked, we need to execute an action (switch to other scene)
        Issue: How do we track which button was clicked and which action to execute?
        
        1. Init a main menu
        2. User clicks button on the main menu
        3. Find out which button he clicked
        4. Find out to which menu should this button lead
        5. Create (show) next menu
        
    """        
