# MIT License
# Ported from the C++ library by DFRobot: https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299
# Adapted and porting assistance provided by ChatGPT-3.5, an AI language model developed by OpenAI.
# https://openai.com

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import board
import busio

class DFPlayerMini:
    def __init__(self, uart):
        """
        Initialize the DFPlayerMini object with the given UART object.

        Parameters:
        - uart (UART): The UART object used to communicate with the DFPlayer Mini module.

        This method initializes the DFPlayer Mini module by sending the necessary
        initialization commands over the UART communication. It verifies the
        communication with the module and sets the default configuration, such as
        volume, equalizer, and output device.

        Note: Make sure to set the correct baud rate (9600) on the UART object before
        initializing the DFPlayerMini object.
        """
        self.uart = uart
        # self.uart.init(9600) # Human edit: needed to comment this out for the module to work when using pyserial

        print("Initializing DFPlayer... (May take 3~5 seconds)")

        self.send_cmd(0x00)  # Send command: Initialize the module

        response, data = self.read_response() # Humanedit: fixed
        if response == b'\x7E\xFF\x06\x00\x00\x00\xFE\xEF':
            print("DFPlayer Mini online.")
        else:
            print("DFPlayer initialization failed.")
            return

        self.send_cmd(0x06, 0x00, 0x00)  # Send command: Set serial communication time out (500ms)

        response, data = self.read_response() # Humanedit: fixed
        if response == b'\x7E\xFF\x06\x00\x00\x00\xFE\xEF':
            print("DFPlayer time out set to 500ms.")
        else:
            print("Failed to set time out.")
            return

        self.set_volume(10)  # Set initial volume (0 to 30)
        self.set_eq(0)  # Set equalizer mode to normal
        self.set_output_device(3)  # Set output device to SD card (3)

        print("DFPlayer initialized.")
        
        
    def send_cmd(self, cmd, param1=0, param2=0):
        """
        Send a command to the DFPlayer Mini MP3 module via UART.

        Parameters:
            - cmd (int): The command code to be sent to the DFPlayer module.
            - param1 (int, optional): The first parameter associated with the command (default is 0).
            - param2 (int, optional): The second parameter associated with the command (default is 0).

        Command Byte Array Structure:
            [0x7E, 0xFF, 0x06, cmd, 0x01, param1, param2, 0xEF]

            - 0x7E: Start of transmission command.
            - 0xFF: Fixed version byte.
            - 0x06: The number of bytes in the command (excluding start and end bytes).
            - cmd: The command code to be executed by the DFPlayer module.
            - 0x01: The index of the module (reserved for future use, set to 0x01).
            - param1: The first parameter value associated with the command (if required).
            - param2: The second parameter value associated with the command (if required).
            - 0xEF: End of transmission command.

        Note:
            - The DFPlayer module expects specific command codes to perform various actions, and additional
              parameters may be required for certain commands (e.g., setting volume, selecting EQ, etc.).
            - Refer to the DFPlayer Mini documentation for a list of available commands and their details.
        """
    
        buf = bytearray([0x7E, 0xFF, 0x06, cmd, 0x01, param1, param2, 0xEF])
        self.uart.write(buf)

    def set_volume(self, volume):
        """Set the volume of the DFPlayer Mini module.
        Command: 0x06
        Parameters: Volume (0 to 30)
        """
        volume_byte = min(max(volume, 0), 30).to_bytes(1, byteorder='big')
        self.send_cmd(0x06, 0x00, volume_byte)

    def volume_up(self):
        """Increase the volume of the DFPlayer Mini module.
        Command: 0x04
        """
        self.send_cmd(0x04)

    def volume_down(self):
        """Decrease the volume of the DFPlayer Mini module.
        Command: 0x05
        """
        self.send_cmd(0x05)

    def set_eq(self, eq):
        """Set the equalizer mode of the DFPlayer Mini module.
        Command: 0x07
        Parameters: EQ Mode (0 for NORMAL, 1 for POP, 2 for ROCK, 3 for JAZZ, 4 for CLASSIC, 5 for BASS)
        """
        eq_byte = min(max(eq, 0), 5).to_bytes(1, byteorder='big')
        self.send_cmd(0x07, 0x00, eq_byte)

    def set_output_device(self, device):
        """Set the output device of the DFPlayer Mini module.
        Command: 0x09
        Parameters: Output Device (0 for U_DISK, 1 for SD, 2 for AUX, 3 for SLEEP, 4 for FLASH)
        """
        device_byte = min(max(device, 0), 4).to_bytes(1, byteorder='big')
        self.send_cmd(0x09, 0x00, device_byte)

    def play_track(self, track):
        """Play a specific track on the DFPlayer Mini module.
        Command: 0x03
        Parameters: Track Number (0 to 65535)
        """
        track_bytes = min(max(track, 0), 65535).to_bytes(2, byteorder='big')
        self.send_cmd(0x03, track_bytes[0], track_bytes[1])

    def loop_track(self, track):
        """Loop a specific track on the DFPlayer Mini module.
        Command: 0x08
        Parameters: Track Number (0 to 65535)
        """
        track_bytes = min(max(track, 0), 65535).to_bytes(2, byteorder='big')
        self.send_cmd(0x08, track_bytes[0], track_bytes[1])

    def pause(self):
        """Pause the currently playing track on the DFPlayer Mini module.
        Command: 0x0E
        """
        self.send_cmd(0x0E)

    def start(self):
        """Start/resume playing the track on the DFPlayer Mini module.
        Command: 0x0D
        """
        self.send_cmd(0x0D)

    def play_folder_track(self, folder, track):
        """Play a specific track in a folder on the DFPlayer Mini module.
        Command: 0x0F
        Parameters: Folder Name (1 to 99), Track Number (1 to 255)
        """
        self.send_cmd(0x0F, folder, track)

    def enable_loop_all(self):
        """Enable loop mode for all tracks on the DFPlayer Mini module.
        Command: 0x11
        Parameters: 0x01
        """
        self.send_cmd(0x11, 0x00, 0x01)

    def disable_loop_all(self):
        """Disable loop mode for all tracks on the DFPlayer Mini module.
        Command: 0x11
        Parameters: 0x00
        """
        self.send_cmd(0x11, 0x00, 0x00)

    def play_mp3_track(self, track):
        """Play a specific MP3 track on the DFPlayer Mini module.
        Command: 0x12
        Parameters: Track Number (0x00 to 0xFFFF)
        """
        self.send_cmd(0x12, 0x00, track)

    def advertise_track(self, track):
        """Advertise a specific track on the DFPlayer Mini module.
        Command: 0x13
        Parameters: Track Number (0x00 to 0xFFFF)
        """
        self.send_cmd(0x13, 0x00, track)

    def stop_advertise(self):
        """Stop advertising on the DFPlayer Mini module.
        Command: 0x15
        """
        self.send_cmd(0x15)

    def play_large_folder_track(self, folder, track):
        """Play a specific track in a large folder on the DFPlayer Mini module.
        Command: 0x14
        Parameters: Folder Name (1 to 10), Track Number (1 to 1000)
        """
        self.send_cmd(0x14, folder, track)

    def loop_folder(self, folder):
        """Loop all tracks in a specific folder on the DFPlayer Mini module.
        Command: 0x17
        Parameters: Folder Name (1 to 99)
        """
        self.send_cmd(0x17, 0x00, folder)

    def random_all(self):
        """Play all tracks in random order on the DFPlayer Mini module.
        Command: 0x18
        """
        self.send_cmd(0x18)

    def enable_loop(self):
        """Enable loop mode for the current track on the DFPlayer Mini module.
        Command: 0x19
        Parameters: 0x01
        """
        self.send_cmd(0x19, 0x00, 0x01)

    def disable_loop(self):
        """Disable loop mode for the current track on the DFPlayer Mini module.
        Command: 0x19
        Parameters: 0x00
        """
        self.send_cmd(0x19, 0x00, 0x00)

    def read_response(self): # Humanedit, this method was missing, asked to recreate it
        """
        Reads and parses the response from the DFPlayer module.

        :return: The response code and any additional data received.
        :rtype: tuple[int, bytes]
        """
        response = self.uart.read(10)  # Assuming the response will be no more than 10 bytes
        if response:
            # Parse the response
            response_code = response[3]
            data_length = response[5] - 2  # Subtract 2 for the command and checksum bytes
            data = self.uart.read(data_length) if data_length > 0 else b''

            # Read the checksum byte
            checksum = self.uart.read(1)

            # Verify the checksum
            checksum_calc = sum(response[1:7]) + sum(data)
            checksum_calc = (~checksum_calc) & 0xFF
            if checksum_calc == int.from_bytes(checksum, byteorder='big'):
                return response_code, data
            else:
                print("Checksum error in response!")
        return None, None

    def read_state(self):
        """Read the current state of the DFPlayer Mini module.
        Command: 0x42
        """
        self.send_cmd(0x42)
        return self.uart.read(10)

    def read_volume(self):
        """Read the current volume level of the DFPlayer Mini module.
        Command: 0x43
        """
        self.send_cmd(0x43)
        return self.uart.read(10)

    def read_eq(self):
        """Read the current equalizer mode of the DFPlayer Mini module.
        Command: 0x44
        """
        self.send_cmd(0x44)
        return self.uart.read(10)

    def read_file_counts(self):
        """Read the total number of files in the SD card of the DFPlayer Mini module.
        Command: 0x47
        """
        self.send_cmd(0x47)
        return self.uart.read(10)

    def read_current_file_number(self):
        """Read the current file number being played on the DFPlayer Mini module.
        Command: 0x4B
        """
        self.send_cmd(0x4B)
        return self.uart.read(10)

    def read_file_counts_in_folder(self, folder):
        """Read the total number of files in a specific folder on the DFPlayer Mini module.
        Command: 0x48
        Parameters: Folder Name (1 to 99)
        """
        self.send_cmd(0x48, 0x00, folder)
        return self.uart.read(10)
