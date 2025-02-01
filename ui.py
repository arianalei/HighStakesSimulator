import pygame
import pygame_gui

pygame.init()

class UserInterface:
    def __init__(self, ui_manager, game):
        self.ui_manager = ui_manager

        # UI Elements
        self.command_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((920, 50), (260, 30)),
            text="Command to be executed:",
            manager=self.ui_manager
        )

        # Multiline Editable Text Box
        self.command_input = pygame_gui.elements.UITextEntryBox(
            relative_rect=pygame.Rect((920, 100), (260, 250)),  # Adjusted for size
            manager=self.ui_manager
        )

        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((920, 370), (120, 40)),
            text="Reset",
            manager=self.ui_manager
        )
        self.run_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((1060, 370), (120, 40)),
            text="Run",
            manager=self.ui_manager
        )

        self.load_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((920, 800), (260, 40)),
            text="Load Commands",
            manager=self.ui_manager
        )   

    def get_commands(self):
        """Retrieve the text input from the editable text box."""
        return self.command_input.get_text().strip()

    def set_commands(self, text):
        """Set the text in the editable text box."""
        self.command_input.set_text(text)
        
    def load_commands_from_file(self, file_path):
        print(f"Loading commands from {file_path}")
        try:
            with open(file_path, 'r') as file:
                commands = file.read()
                self.command_input.set_text("")  # Clear existing input
                self.command_input.set_text(commands)  # Load new content
                
                print(f"Commands loaded from {file_path}")
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"Error loading file: {e}")