import pygame
import math

class Robot:
    def __init__(self):
        self.real_x = 500  # Initial position (real coordinates in mm, centered)
        self.real_y = 1800
        self.head_axis = (-1, 0)  # Initial heading axis (facing left, x = -1, y = 0)
        self.color = (0, 0, 255)
        self.size = 460  # Robot size in mm

        self.velocity = 0
        self.target_distance = 0
        self.distance_traveled = 0
        self.turn_speed = 0
        self.target_angle = 0
        self.turn_angle = 0

        # Load the robot image
        half_size = self.size / (2 * 4)  # Half the size, scaled to the screen
        self.robot_image = pygame.image.load('./images/robot.png')
        self.robot_image = pygame.transform.scale(self.robot_image, (int(2 * half_size), int(2 * half_size)))

    def reset(self):
        """Reset the robot to its initial position and orientation."""
        self.real_x = 500
        self.real_y = 1800
        self.head_axis = (-1, 0)  # Reset to initial heading (facing left)

        self.velocity = 0
        self.target_distance = 0
        self.distance_traveled = 0
        self.turn_speed = 0
        self.target_angle = 0
        self.turn_angle = 0
        print("Robot reset to initial position and orientation.")

    def start_run(self, velocity, heading_degrees, distance):
        """Start moving in a straight line."""
        # Convert the heading angle (in degrees) to a unit vector (heading axis)
        radians = - math.radians(heading_degrees)
        self.head_axis = (math.cos(radians), math.sin(radians))  # Unit vector for heading

        # Normalize the heading axis to ensure it is a unit vector
        magnitude = math.sqrt(self.head_axis[0]**2 + self.head_axis[1]**2)
        self.head_axis = (self.head_axis[0] / magnitude, self.head_axis[1] / magnitude)

        self.velocity = - velocity * 5  # Scale velocity by 5 to make movement faster
        self.target_distance = distance
        self.distance_traveled = 0

    def update_run(self, time_delta):
        """Update straight-line movement."""
        # Check if the target distance has been reached
        if self.distance_traveled >= self.target_distance:
            self.velocity = 0
            return True

        # Calculate the distance to travel in the current frame
        distance_to_travel = self.velocity * time_delta
        remaining_distance = self.target_distance - self.distance_traveled

        # Ensure the robot doesn't overshoot the target distance
        if distance_to_travel > remaining_distance:
            distance_to_travel = remaining_distance

        self.distance_traveled += distance_to_travel

        # Update the robot's real-world coordinates based on head axis
        self.real_x += distance_to_travel * self.head_axis[0]
        self.real_y += distance_to_travel * self.head_axis[1]

        return False

    def start_turn(self, target_angle, velocity):
        """Start turning to align with the canonical heading direction."""
        # Calculate the required rotation angle from the canonical direction
        current_angle = math.degrees(math.atan2(self.head_axis[1], self.head_axis[0]))
        rotation_needed = target_angle - current_angle

        # Normalize the rotation angle to the range [-180, 180] for shortest rotation
        rotation_needed = (rotation_needed + 180) % 360 - 180

        self.target_angle = rotation_needed  # Absolute rotation to perform
        self.turn_speed = velocity * 5  # Scale turn speed by 5
        self.turn_angle = 0  # Reset the accumulated turn angle

    def update_turn(self, time_delta):
        """Update turning movement based on the canonical direction."""
        if abs(self.turn_angle) >= abs(self.target_angle):
            self.turn_speed = 0

            # Update the canonical heading to match the target direction
            radians = math.radians(self.target_angle)
            self.head_axis = (math.cos(radians), math.sin(radians))
            return True

        # Calculate the angle to turn in the current frame
        angle_to_turn = self.turn_speed * time_delta
        angle_to_turn = min(angle_to_turn, abs(self.target_angle - self.turn_angle)) * (
            1 if self.target_angle > self.turn_angle else -1
        )
        self.turn_angle += angle_to_turn

        # Incrementally update the heading axis during the turn
        radians = math.radians(angle_to_turn)
        cos_turn = math.cos(radians)
        sin_turn = math.sin(radians)

        new_x = self.head_axis[0] * cos_turn - self.head_axis[1] * sin_turn
        new_y = self.head_axis[0] * sin_turn + self.head_axis[1] * cos_turn
        self.head_axis = (new_x, new_y)
        return False
    
    def draw(self, screen, real_to_screen):
        """Draw the robot on the screen with an image overlay and a direction line."""
        screen_x, screen_y = real_to_screen(self.real_x, self.real_y)
        half_size = self.size / (2 * 4)  # Half the size, scaled to the screen

        # Rotate the image based on the head axis direction
        angle = math.degrees(math.atan2(self.head_axis[1], self.head_axis[0]))  # Convert head axis to angle
        rotated_image = pygame.transform.rotate(self.robot_image, -angle)

        # Get the rotated image's new rectangle and set its center to the robot's position
        rotated_rect = rotated_image.get_rect(center=(screen_x, screen_y))

        # Draw the robot image
        screen.blit(rotated_image, rotated_rect.topleft)

        # Calculate the end point of the direction line
        end_x = screen_x + half_size * self.head_axis[0]
        end_y = screen_y + half_size * self.head_axis[1]

        # Draw the direction line
        pygame.draw.line(screen, (255, 255, 255), (screen_x, screen_y), (end_x, end_y), 2)


