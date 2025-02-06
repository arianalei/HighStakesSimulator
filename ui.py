import pygame
import pygame_gui
import tkinter as tk
from tkinter import filedialog

pygame.init()

class UserInterface:
    def __init__(self, ui_manager, game):
        self.ui_manager = ui_manager
        self.game = game

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
            relative_rect=pygame.Rect((920, 800), (260, 40)),  # Adjust position as needed
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
        """Loads commands from the specified file into the command input."""
        try:
            with open(file_path, 'r') as file:
                commands = file.read()
                self.command_input.set_text(commands)  # Set loaded commands into the command input
                self.game.reset_robot()  # Reset robot as per previous requirements
                self.game.reset_timer()  # Reset timer if necessary
                print(f"Commands loaded from {file_path}")
        except Exception as e:
            print(f"Error loading file: {e}")

    def open_file_dialog(self):
        """Opens a file dialog, allowing the user to choose a file to load commands from."""
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        file_path = filedialog.askopenfilename()  # Open the file dialog
        if file_path:
            self.load_commands_from_file(file_path)
        root.destroy()