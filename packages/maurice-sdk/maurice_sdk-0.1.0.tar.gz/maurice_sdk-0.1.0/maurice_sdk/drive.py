"""
drive.py

Synchronous UART interface for drive control.
Provides methods to set speed and get position without using a separate thread.
"""

import serial
import struct
import time

# Protocol Constants
SOM_MARKER = bytes([0x69, 0x69])
CMD_MOVE = 0x01      # Command to set drive speed.
RESP_MOVE = 0x81     # Response carrying position update.

# CRC-8/MAXIM Constants
CRC8_POLY = 0x8C
CRC8_INIT = 0x00

class Drive:
    def __init__(self, port: str, baud_rate: int = 115200, timeout: float = 0.1):
        """
        Initializes the synchronous UART drive interface.
        
        :param port: Serial port device (e.g., '/dev/ttyTHS1')
        :param baud_rate: Baud rate for communication.
        :param timeout: Read timeout in seconds.
        """
        self.ser = serial.Serial(port, baud_rate, timeout=timeout)
        self.last_position = None  # Stores the most recent (x, y, theta) update

    def _calculate_crc(self, data: bytes) -> int:
        """
        Calculate the CRC-8/MAXIM value for the given data.
        """
        crc = CRC8_INIT
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x01:
                    crc = (crc >> 1) ^ CRC8_POLY
                else:
                    crc >>= 1
        return crc

    def _send_command(self, cmd_id: int, payload: bytes) -> None:
        """
        Builds and sends a command packet.
        Packet layout: [SOM (2 bytes)] + [cmd_id (1 byte)] + [payload (6 bytes)] + [CRC (1 byte)]
        
        :param cmd_id: Command identifier.
        :param payload: Exactly 6 bytes of payload.
        """
        if len(payload) != 6:
            raise ValueError("Payload must be exactly 6 bytes.")
        protocol_msg = bytes([cmd_id]) + payload  # 7 bytes total
        crc = self._calculate_crc(protocol_msg)
        packet = SOM_MARKER + protocol_msg + bytes([crc])
        self.ser.write(packet)

    def _read_packet(self, timeout: float = 0.1):
        """
        Reads a complete packet from the serial port using a simple state machine.
        
        :param timeout: Maximum time to wait for a complete packet.
        :return: Tuple (msg_id, data) if a valid packet is received; otherwise, None.
        """
        start_time = time.time()
        buffer = bytearray()
        while time.time() - start_time < timeout:
            if self.ser.in_waiting:
                buffer.extend(self.ser.read(self.ser.in_waiting))
            # Look for the start-of-message marker in the buffer.
            if len(buffer) >= 2:
                som_index = buffer.find(SOM_MARKER)
                if som_index != -1 and len(buffer) >= som_index + 10:
                    packet = buffer[som_index : som_index + 10]
                    # Remove processed bytes from the buffer.
                    buffer = buffer[som_index + 10:]
                    # Validate packet (last byte is CRC for bytes [2:9]).
                    protocol_msg = packet[2:9]  # 7 bytes: cmd_id + payload
                    #print(f"Received packet: {protocol_msg}")
                    computed_crc = self._calculate_crc(protocol_msg)
                    received_crc = packet[9]
                    if computed_crc == received_crc:
                        msg_id = protocol_msg[0]
                        data = protocol_msg[1:]
                        return msg_id, data
                    # If CRC fails, continue waiting.
            time.sleep(0.01)
        return None

    def set_speed(self, forward_speed: float, turn_rate: float) -> None:
        """
        Sets the drive speeds by sending a CMD_MOVE command.
        Waits synchronously for a response packet (RESP_MOVE) containing the position update.
        
        :param forward_speed: Forward speed in m/s. (Scaled by 100.)
        :param turn_rate: Turn rate in rad/s. (Scaled by 100.)
        """
        # Scale speeds to integer representation.
        speed_int = int(forward_speed * 100)
        turn_int = int(turn_rate * 100)
        # Build payload: 2 bytes forward speed, 2 bytes turn rate, 2 reserved bytes (set to 0).
        payload = struct.pack(">hhH", speed_int, turn_int, 0)
        self._send_command(CMD_MOVE, payload)
        # Synchronously wait for a response packet.
        #time.sleep(0.02)
        packet = self._read_packet(timeout=0.1)
        if packet is not None:
            print(f"Received packet: {packet}")
            msg_id, data = packet
            if msg_id == RESP_MOVE:
                try:
                    # Unpack the response: x, y, theta (each 2 bytes, signed).
                    x, y, theta = struct.unpack(">hhh", data)
                    # Convert to meaningful units (assuming x, y in mm and theta in hundredths of a radian).
                    self.last_position = (x / 1000.0, y / 1000.0, theta / 100.0)
                except struct.error:
                    self.last_position = None
            else:
                self.last_position = None
        else:
            self.last_position = None

    def get_position(self):
        """
        Returns the last received position update.
        
        :return: Tuple (x, y, theta) or None if no valid update is available.
        """
        return self.last_position

    def close(self):
        """
        Closes the serial port connection.
        """
        if self.ser.is_open:
            self.ser.close()


# Example usage:
if __name__ == "__main__":
    # Update the port with the correct serial device for your system.
    drive = Drive(port="/dev/ttyTHS1", baud_rate=115200, timeout=0.1)
    
    # Set speed (e.g., forward_speed=0.5 m/s, turn_rate=0.1 rad/s) and get the position update.
    drive.set_speed(0.5, 0.1)
    position = drive.get_position()
    print("Position:", position)
    
    drive.close()
