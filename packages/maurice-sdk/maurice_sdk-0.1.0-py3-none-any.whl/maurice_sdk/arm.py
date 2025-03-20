"""
arm.py

High-level interface for controlling a robotic arm with Dynamixel servos.
Provides individual servo commands and arm-level (group) operations.
"""

from typing import List, Dict
import time

# Import lower-level modules from your package.
from maurice_sdk.dynamixel import Dynamixel, OperatingMode, ReadAttribute
from maurice_sdk.robot import Robot

class Arm:
    def __init__(self, device_name: str, baudrate: int, servo_ids: List[int]):
        """
        Initializes the Arm interface.
        
        :param device_name: Serial port device name (e.g., '/dev/ttyUSB0')
        :param baudrate: Baud rate for communication (e.g., 57600 or 1_000_000)
        :param servo_ids: List of servo IDs in the arm (e.g., [1, 2, 3, 4, 5])
        """
        # Create a Dynamixel instance (using the first servo id for initialization).
        config = Dynamixel.Config(
            baudrate=baudrate,
            device_name=device_name,
            dynamixel_id=servo_ids[0]
        )
        self.dynamixel = Dynamixel(config)
        self.servo_ids = servo_ids
        # Create a Robot instance for group operations like goal positions and reading positions.
        self.robot = Robot(self.dynamixel, baudrate=baudrate, servo_ids=servo_ids)

    # ----- Individual Servo Methods -----

    def set_operating_mode(self, servo_id: int, mode: OperatingMode) -> None:
        """
        Sets the operating mode for a single servo.
        
        :param servo_id: ID of the servo.
        :param mode: Operating mode (e.g., OperatingMode.POSITION or OperatingMode.PWM).
        """
        self.dynamixel.set_operating_mode(servo_id, mode)

    def set_joint_limit(self, servo_id: int, min_position: int, max_position: int) -> None:
        """
        Sets the joint limits for a single servo.
        
        :param servo_id: ID of the servo.
        :param min_position: Minimum allowed position.
        :param max_position: Maximum allowed position.
        """
        self.dynamixel.set_min_position_limit(servo_id, min_position)
        self.dynamixel.set_max_position_limit(servo_id, max_position)

    def enable_torque(self, servo_id: int) -> None:
        """
        Enables torque for a single servo.
        
        :param servo_id: ID of the servo.
        """
        self.dynamixel._enable_torque(servo_id)

    def disable_torque(self, servo_id: int) -> None:
        """
        Disables torque for a single servo.
        
        :param servo_id: ID of the servo.
        """
        self.dynamixel._disable_torque(servo_id)

    def set_current_limit(self, servo_id: int, current_limit: int) -> None:
        """
        Sets the current limit for a single servo.
        
        :param servo_id: ID of the servo.
        :param current_limit: Current limit in mA.
        """
        self.dynamixel.set_current_limit(servo_id, current_limit)

    # ----- Arm-Level Methods -----

    def set_goal_positions(self, positions: List[int]) -> None:
        """
        Sets the goal positions for all servos in the arm.
        
        :param positions: List of target positions for each servo.
                          Length must match the number of servos.
        """
        if len(positions) != len(self.servo_ids):
            raise ValueError("Length of positions list must match number of servos.")
        self.robot.set_goal_pos(positions)

    def read_positions(self) -> List[int]:
        """
        Reads and returns the current positions of all servos in the arm.
        
        :return: List of positions for each servo.
        """
        return self.robot.read_position()

    def read_voltages(self) -> Dict[int, int]:
        """
        Reads the voltage value from each servo.
        
        Note: Voltage is read as a raw value using ReadAttribute.VOLTAGE.
              Conversion may be necessary depending on your setup.
        
        :return: Dictionary mapping each servo ID to its voltage reading.
        """
        voltages = {}
        for servo_id in self.servo_ids:
            voltage = self.dynamixel._read_value(servo_id, ReadAttribute.VOLTAGE, 1)
            voltages[servo_id] = voltage
        return voltages

    def torque_on(self) -> None:
        """
        Enables torque for all servos in the arm.
        """
        for servo_id in self.servo_ids:
            self.enable_torque(servo_id)
        time.sleep(0.05)  # Short delay to ensure settings are applied

    def torque_off(self) -> None:
        """
        Disables torque for all servos in the arm.
        """
        for servo_id in self.servo_ids:
            self.disable_torque(servo_id)
        time.sleep(0.05)

    def close(self) -> None:
        """
        Disconnects from the Dynamixel bus.
        """
        self.dynamixel.disconnect()


# Example usage (if needed for testing):
if __name__ == "__main__":
    # Replace with appropriate values for your setup.
    device = "/dev/ttyUSB0"
    baud = 57600
    servo_ids = [1, 2, 3, 4, 5]

    arm = Arm(device, baud, servo_ids)

    # Example individual servo control:
    arm.set_operating_mode(servo_ids[0], OperatingMode.POSITION)
    arm.set_joint_limit(servo_ids[0], 0, 4095)
    arm.set_current_limit(servo_ids[0], 1500)
    arm.enable_torque(servo_ids[0])
    time.sleep(0.5)
    arm.disable_torque(servo_ids[0])

    # Example arm-level control:
    arm.torque_on()
    arm.set_goal_positions([2048, 2048, 2048, 2048, 2048])
    positions = arm.read_positions()
    voltages = arm.read_voltages()
    print("Positions:", positions)
    print("Voltages:", voltages)
    arm.torque_off()

    # Close connection when done
    arm.close()
