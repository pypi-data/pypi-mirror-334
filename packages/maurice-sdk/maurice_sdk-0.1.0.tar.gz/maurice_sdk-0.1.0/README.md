# Maurice SDK

Maurice SDK is a Python package designed to control a robotic arm using Dynamixel servos. The package provides both low-level and high-level APIs to manage individual servo settings (operating mode, joint limits, torque, current limit) as well as group operations for the entire arm (goal positions, position readings, voltage readings, torque control). Additionally, it offers a synchronous drive interface via UART to set speeds and receive position updates.

## Features

- **Individual Servo Control:**
  - Set operating mode (e.g., POSITION or PWM)
  - Configure joint limits (min and max positions)
  - Enable/disable torque
  - Set current limits

- **Arm-Level Control:**
  - Set goal positions for all servos in the arm
  - Read current positions
  - Retrieve voltage readings for each servo
  - Toggle torque for the entire arm

- **Drive Interface:**
  - Synchronously send speed commands over UART
  - Receive and parse position update responses

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd maurice_sdk
