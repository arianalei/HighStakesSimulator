import pygame
import math

class Robot:
    def __init__(self):
        self.type = "Skills Auton"  # Default type of robot

        self.reset()

        self.color = (0, 0, 255)
        self.size = 460  # Robot size in mm

        self.friction_factor = 0.62  # Friction factor for velocity decay
        self.velocity_factor = 14  # Velocity increase factor to mimic real-world behavior

        # Load the robot image
        half_size = self.size / (2 * 4)  # Half the size, scaled to the screen
        self.robot_image = pygame.image.load('./images/robot.png')
        self.robot_image = pygame.transform.scale(self.robot_image, (int(2 * half_size), int(2 * half_size)))

    def reset(self):
        """Reset the robot to its initial position and orientation."""
        self.reset_position()

        self.velocity = 0
        self.target_distance = 0
        self.distance_traveled = 0
        self.turn_speed = 0
        self.target_angle = 0
        self.turn_angle = 0
        print("Robot reset to initial position and orientation.")

    def reset_position(self):
        # Define a lookup dictionary with type as key and (real_x, real_y) as value
        position_lookup = {
            "Skills Auton": (500, 1800, (-1, 0), (-1, 0)),
            "Alliance Red Right": (500, 2650, (1, 0), (1, 0)),
            "Alliance Red Left": (500, 1400, (1, 0), (1, 0)),
            "Alliance Blue Right": (1800, 2650, (-1, 0), (-1, 0)),
            "Alliance Blue Left": (1800, 1400, (-1, 0), (-1, 0))
        }
        # Get the position from the lookup dictionary or use default values
        self.real_x, self.real_y, self.head_axis, self.cannonical_heading = position_lookup.get(self.type, (500, 1800, (-1, 0), (-1, 0)))

    def set_type(self, type):
        self.type = type

    def start_run(self, velocity, heading_degrees, distance):
        """Start moving in a straight line."""
        print(f"Starting run: velocity={velocity}, heading={heading_degrees}, distance={distance}")

        # Convert the heading angle (in degrees) to a unit vector (heading axis)
        # Change here: No negation, and adjust by adding 180 degrees if you want (-1, 0) for 0 degrees
        radians = math.radians(heading_degrees + 180)
        self.head_axis = (math.cos(radians), math.sin(radians))  # Unit vector for heading
        print(f"Head axis: {self.head_axis}")

        # Set velocity (backward or forward depending on the sign)
        self.velocity = velocity * self.velocity_factor  # Scale velocity by a factor
        self.target_distance = self.friction_factor * abs(distance)  # Use the absolute distance to track movement
        self.distance_traveled = 0

    def update_run(self, time_delta):
        """Update straight-line movement."""
        # Check if the target distance has been reached
        if self.distance_traveled >= self.target_distance:
            self.velocity = 0
            return True

        # Calculate the distance to travel in the current frame
        distance_to_travel = abs(self.velocity) * time_delta
        remaining_distance = self.target_distance - self.distance_traveled

        # Ensure the robot doesn't overshoot the target distance
        if distance_to_travel > remaining_distance:
            distance_to_travel = remaining_distance

        self.distance_traveled += distance_to_travel

        # Update the robot's real-world coordinates based on head axis and the direction of movement
        direction_multiplier = -1 if self.velocity < 0 else 1
        self.real_x += direction_multiplier * distance_to_travel * self.head_axis[0]
        self.real_y += direction_multiplier * distance_to_travel * self.head_axis[1]

        return False

    def start_turn(self, target_angle, velocity):
        """Start turning to align with the canonical heading direction."""
        # Calculate the required rotation angle from the canonical direction
        current_angle = math.degrees(math.atan2(self.head_axis[1], self.head_axis[0]))
        rotation_needed = target_angle - current_angle

        # Normalize the rotation angle to the range [-180, 180] for shortest rotation
        rotation_needed = (rotation_needed + 180) % 360 - 180

        self.target_angle = rotation_needed  # Absolute rotation to perform
        self.turn_speed = velocity * self.velocity_factor  # Scale turn speed by a factor
        self.turn_angle = 0  # Reset the accumulated turn angle

    def update_turn(self, time_delta):
        """Update turning movement based on the canonical direction."""
        if abs(self.turn_angle) >= abs(self.target_angle):
            self.turn_speed = 0
            return True  # Stop turning as we have reached or exceeded the target angle

        # Calculate the angle to turn in the current frame, ensuring we do not exceed the target angle
        angle_to_turn = self.turn_speed * time_delta
        remaining_angle = abs(self.target_angle) - abs(self.turn_angle)
        angle_to_turn = min(angle_to_turn, remaining_angle) * (1 if self.target_angle > self.turn_angle else -1)
        self.turn_angle += angle_to_turn

        # Incrementally update the heading axis during the turn
        radians = math.radians(angle_to_turn)
        cos_turn = math.cos(radians)
        sin_turn = math.sin(radians)
        new_x = self.head_axis[0] * cos_turn - self.head_axis[1] * sin_turn
        new_y = self.head_axis[0] * sin_turn + self.head_axis[1] * cos_turn

        # Normalize the heading to maintain consistent direction accuracy
        self.head_axis = (new_x, new_y)
        magnitude = math.sqrt(self.head_axis[0]**2 + self.head_axis[1]**2)
        self.head_axis = (self.head_axis[0] / magnitude, self.head_axis[1] / magnitude)

        print(f"Updated head axis during turning: {self.head_axis}")
        return False


    def draw(self, screen, real_to_screen):
        """Draw the robot on the screen with an image overlay and an isosceles triangle for the front."""
        screen_x, screen_y = real_to_screen(self.real_x, self.real_y)
        half_size = self.size / (2 * 4)  # Half the size, scaled to the screen

        # Rotate the image based on the head axis direction
        angle = math.degrees(math.atan2(self.head_axis[1], self.head_axis[0]))  # Convert head axis to angle
        rotated_image = pygame.transform.rotate(self.robot_image, -angle)

        # Get the rotated image's new rectangle and set its center to the robot's position
        rotated_rect = rotated_image.get_rect(center=(screen_x, screen_y))

        # Draw the robot image
        screen.blit(rotated_image, rotated_rect.topleft)

        # Calculate the front triangle points
        # Perpendicular vector to the head axis (left and right offsets for the corners)
        perpendicular_axis = (-self.head_axis[1], self.head_axis[0])  # Rotate head axis 90 degrees

        # Calculate the two front corners of the robot
        front_left_x = screen_x + half_size * self.head_axis[0] - half_size * 0.5 * perpendicular_axis[0]
        front_left_y = screen_y + half_size * self.head_axis[1] - half_size * 0.5 * perpendicular_axis[1]

        front_right_x = screen_x + half_size * self.head_axis[0] + half_size * 0.5 * perpendicular_axis[0]
        front_right_y = screen_y + half_size * self.head_axis[1] + half_size * 0.5 * perpendicular_axis[1]

        # Define the triangle points: center of the robot and two front corners
        triangle_points = [
            (screen_x, screen_y),  # Center of the robot
            (front_left_x, front_left_y),  # Front left corner
            (front_right_x, front_right_y),  # Front right corner
        ]

        # Draw the triangle outline for a thicker line effect
        pygame.draw.lines(screen, (255, 255, 255), True, triangle_points, 2)  # White outline with 2px thicknes

