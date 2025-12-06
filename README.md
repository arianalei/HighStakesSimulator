# High Stakes Simulator

A 2D robot simulation environment for testing and visualizing VEX VRC (VEX Robotics Competition) autonomous routines. This simulator allows you to test robot movement commands, visualize paths on the competition field, and verify autonomous sequences before deploying to physical robots.

**Repository**: [https://github.com/arianalei/HighStakesSimulator](https://github.com/arianalei/HighStakesSimulator)

## Demo

![Simulator in Action](images/robot_in_action.gif)

## Features

- **Visual Field Simulation**: Interactive 2D visualization of the VEX VRC High Stakes field
- **Command Queue System**: Execute multiple commands in sequence
- **Multiple Starting Positions**: Support for Skills Auton and Alliance match starting positions
- **Real-time Timer**: Track execution time of autonomous routines
- **File Loading**: Load command sequences from text files
- **Command Syntax**: Supports `rundis`, `turnaround`, and `wait` commands with comments

## Installation

### Requirements

- Python 3.6 or higher
- pygame
- pygame_gui

### Setup

1. **Install Python** (if not already installed)
   - Download from [python.org](https://www.python.org/downloads/)
   - Follow installation instructions for your operating system

2. **Install Required Libraries**
   ```bash
   pip install pygame pygame_gui
   ```

3. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/arianalei/HighStakesSimulator.git
   cd HighStakesSimulator
   ```
   
   Alternatively, you can download the repository as a ZIP file from [GitHub](https://github.com/arianalei/HighStakesSimulator) and extract it.

## Running the Simulator

Run the simulator by executing:

```bash
python simulator.py
```

The simulator window will open with:
- **Left side**: Visual field display (900x900px)
- **Right side**: Control panel with command input, options, and buttons

## Usage

### Basic Workflow

1. **Select Starting Position**: Choose from the dropdown menu:
   - `Skills Auton` - Default starting position
   - `Alliance Red Right` - Red alliance, right starting position
   - `Alliance Red Left` - Red alliance, left starting position
   - `Alliance Blue Right` - Blue alliance, right starting position
   - `Alliance Blue Left` - Blue alliance, left starting position

2. **Enter Commands**: Type or paste commands into the command input box

3. **Run Commands**: Click the "Run" button to execute the command sequence

4. **Reset**: Click the "Reset" button to return the robot to its starting position

5. **Load Commands**: Click "Load Commands" to load a command file from disk

### Command Syntax

The simulator supports three main command types:

#### `rundis(velocity, heading, distance, friction)`
Move the robot in a straight line.

- `velocity`: Movement velocity (positive = forward, negative = backward)
- `heading`: Direction in degrees (0° = right, 90° = up, 180° = left, 270° = down)
- `distance`: Distance to travel in millimeters
- `friction`: Friction factor (typically 0.5)

**Example:**
```
rundis(30, 180, 970, 0.5);  // Move forward at 30 velocity, heading 180°, distance 970mm
rundis(-30, 0, 70, 0.5);    // Move backward at 30 velocity, heading 0°, distance 70mm
```

#### `turnaround(angle, velocity)`
Rotate the robot to a specific heading angle.

- `angle`: Target heading angle in degrees
- `velocity`: Rotation velocity

**Example:**
```
turnaround(90, 30);   // Turn to 90° heading at velocity 30
turnaround(-90, 20);  // Turn to -90° heading at velocity 20
```

#### `wait(time, unit)`
Pause execution for a specified duration.

- `time`: Duration value
- `unit`: Time unit - `sec` (seconds) or `msec` (milliseconds)

**Example:**
```
wait(1, sec);      // Wait 1 second
wait(300, msec);   // Wait 300 milliseconds
```

### Comments

Commands support single-line comments using `//`:

```
// This is a comment
rundis(30, 180, 970, 0.5);  // Move forward
// wait(1, sec);            // This command is commented out
```

### Example Command Sequence

```
// Move backward
rundis(-30, 0, 70, 0.5);
// Turn left 90 degrees
turnaround(-90, 30);
// Wait 300 milliseconds
wait(300, msec);
// Move forward toward mobile goal
rundis(-30, -90, 650, 0.5);
```

## Project Structure

```
HighStakesSimulator/
├── simulator.py          # Main game loop and command execution
├── robot.py              # Robot physics and movement logic
├── field.py              # Field rendering and coordinate conversion
├── ui.py                 # User interface components
├── utils.py              # Utility functions
├── images/               # Field and robot images
│   ├── field_cropped.png
│   ├── field_alliance_cropped.png
│   ├── robot.png
│   └── robot_in_action.gif
└── auto_path/            # Example command files
    ├── commands
    ├── red_left
    ├── red_steal_right
    ├── blue_right
    └── blue_steal_left
```

## Field Specifications

- **Real Field Size**: 3600mm × 3600mm (12ft × 12ft)
- **Screen Display**: 900px × 900px
- **Coordinate System**: 
  - Origin (0, 0) at top-left corner
  - X-axis: left to right (0 to 3600mm)
  - Y-axis: top to bottom (0 to 3600mm)

## Robot Specifications

- **Size**: 460mm (18 inches)
- **Friction Factor**: 0.62 (velocity decay)
- **Velocity Factor**: 14 (scaling factor for realistic movement)

## Tips

- Use the timer display (top-right) to track autonomous routine duration
- The current executing command is displayed at the bottom of the screen
- Commands are executed sequentially from the queue
- Reset the robot and timer before running a new sequence
- Save your command sequences in text files for easy reuse

## Troubleshooting

- **Commands not executing**: Ensure command syntax is correct and ends with semicolon
- **Robot not visible**: Check that the robot image file exists in the `images/` directory
- **Field not displaying**: Verify that field image files exist in the `images/` directory
- **Import errors**: Make sure all required libraries are installed (`pip install pygame pygame_gui`)

## License

[Add your license information here]

## Contributing

[Add contribution guidelines if applicable]
