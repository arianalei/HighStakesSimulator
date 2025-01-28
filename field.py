import pygame
from robot import Robot

class Field:
    def __init__(self, width, height):
        self.width = width  # Screen width (900px)
        self.height = height  # Screen height (900px)
        self.real_width = 3600  # Real field width (3600mm)
        self.real_height = 3600  # Real field height (3600mm)

        # Load and scale the background image
        self.background_image = pygame.image.load('./images/field_cropped.png')
        self.background_image = pygame.transform.scale(self.background_image, (width, height))

        # Overlay for transparency effect
        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((255, 255, 255, int(255 * 0.8)))

        self.robot = Robot()  # The robot object, stored in real-world coordinates

    def real_to_screen(self, real_x, real_y):
        """Convert real field coordinates (mm) to screen coordinates (px)."""
        screen_x = int(real_x / self.real_width * self.width)
        screen_y = int(real_y / self.real_height * self.height)
        return screen_x, screen_y

    def screen_to_real(self, screen_x, screen_y):
        """Convert screen coordinates (px) to real field coordinates (mm)."""
        real_x = screen_x / self.width * self.real_width
        real_y = screen_y / self.height * self.real_height
        return real_x, real_y

    def draw(self, screen):
        """Draw the field, and robot on the screen."""
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.overlay, (0, 0))

        # Draw the robot
        self.robot.draw(screen, self.real_to_screen)

    def reset_robot(self):
        """Reset the robot to its initial position and orientation."""
        self.robot.reset()

    def run_robot_command(self, command):
        """Run a command for the robot."""
        self.robot.execute_command(command)
