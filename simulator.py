import pygame
import pygame_gui
import sys
import math

from field import Field
from ui import UserInterface

class Game:
    def __init__(self):
        pygame.init()

        # Window setup
        self.width, self.height = 1200, 900
        self.field_width, self.field_height = 900, 900
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("High Stakes Emulator")

        # UI Manager
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))

        # Initialize components
        self.field = Field(self.field_width, self.field_height)
        self.ui = UserInterface(self.ui_manager, self)

        # Command queue for robot
        self.command_queue = []
        self.current_command = None
        self.command_start_time = None

        # Clock for frame control
        self.clock = pygame.time.Clock()

    def reset_robot(self):
        self.field.robot.reset()
        print("Robot reset!")

    def parse_command(self, command):
        """Parse and enqueue multiple commands, ignoring commented lines."""
        # Split the input into lines and process each line
        commands = command.splitlines()

        for line in commands:
            # Remove all whitespace, tabs, and line breaks from the line
            line = "".join(line.split())

            # Ignore empty lines
            if not line:
                continue

            # Remove inline comments starting with "//"
            if "//" in line:
                line = line.split("//", 1)[0].strip()

            # Ignore empty lines or commented lines (starting with "//")
            if not line or line.startswith("//"):
                continue

            print(f"Running command: {line}!")

            if line.startswith("rundis"):
                # Example: rundis(30,180,970,0.5);
                params = line[7:-2].split(",")
                velocity = float(params[0])
                heading = float(params[1])
                distance = float(params[2])
                self.command_queue.append(("rundis", velocity, heading, distance))
            elif line.startswith("wait"):
                # Example: wait(1,sec);
                params = line[5:-2].split(",")
                time_value = float(params[0])
                time_unit = params[1].strip()
                time_in_seconds = time_value if time_unit == "sec" else time_value / 1000.0
                self.command_queue.append(("wait", time_in_seconds))
            elif line.startswith("turnaround"):
                # Example: turnaround(180,20);
                params = line[11:-2].split(",")
                angle = float(params[0])
                velocity = float(params[1])
                self.command_queue.append(("turnaround", angle, velocity))

    def execute_next_command(self):
        """Execute the next command in the queue."""
        if not self.command_queue:
            self.current_command = None
            return

        self.current_command = self.command_queue.pop(0)
        self.command_start_time = pygame.time.get_ticks()

        if self.current_command[0] == "wait":
            # No setup needed for wait
            pass
        elif self.current_command[0] == "rundis":
            _, velocity, heading_degrees, distance = self.current_command
            self.field.robot.start_run(velocity, heading_degrees, distance)  # Pass heading as degrees
        elif self.current_command[0] == "turnaround":
            _, target_angle, velocity = self.current_command

            # Ensure the target angle is interpreted as a canonical direction
            current_angle = math.degrees(math.atan2(self.field.robot.head_axis[1], self.field.robot.head_axis[0]))
            rotation_needed = target_angle - current_angle

            # Normalize the rotation angle to the range [-180, 180] for shortest path
            rotation_needed = (rotation_needed + 180) % 360 - 180

            # Start turning to the target canonical direction
            self.field.robot.start_turn(rotation_needed, velocity)

    def update_physics(self, time_delta):
        """Update robot physics for the current command."""
        if not self.current_command:
            self.execute_next_command()
            return

        command_type = self.current_command[0]
        elapsed_time = (pygame.time.get_ticks() - self.command_start_time) / 1000.0

        if command_type == "wait":
            duration = self.current_command[1]
            if elapsed_time >= duration:
                self.execute_next_command()
        elif command_type == "rundis":
            if self.field.robot.update_run(time_delta):
                self.execute_next_command()
        elif command_type == "turnaround":
            if self.field.robot.update_turn(time_delta):
                self.execute_next_command()

    def main_loop(self):
        """Main loop for the game."""
        while True:
            time_delta = self.clock.tick(30) / 1000.0  # Delta time for physics at 30 FPS
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Handle UI events
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.ui.reset_button:
                            self.reset_robot()
                        elif event.ui_element == self.ui.run_button:
                            command = self.ui.command_input.get_text()
                            self.parse_command(command)

                self.ui_manager.process_events(event)

            # Update physics and execute commands
            self.update_physics(time_delta)

            # Draw components
            self.field.draw(self.screen)
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)

            # Update display
            pygame.display.flip()


if __name__ == "__main__":
    game = Game()
    game.main_loop()