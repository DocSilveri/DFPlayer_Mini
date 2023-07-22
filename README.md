# DFPlayerMini Python Library

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/yourusername/dfplayer_mini_python/blob/main/LICENSE)

## Description
Ported from the C++ library provided by [DFRobot](https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299) for the DFPlayer Mini MP3 module. The porting was done with the assistance of ChatGPT-3.5 by OpenAI.

## Prerequisites
- CircuitPython
- CircuitPython compatible board
- DFPlayer Mini MP3 module

## Installation
1. Clone or download this repository.
2. Copy the `dfplayer_mini.py` file to your CircuitPython project directory.

## Usage
1. Import the `DFPlayerMini` class from the library.
2. Create a UART object using the `busio` module and provide it to the `DFPlayerMini` constructor.
3. Use the `DFPlayerMini` methods to control the DFPlayer Mini module.

Example usage:

```python
import time
import board
import busio
from dfplayer_mini import DFPlayerMini

# Create a UART object
uart = busio.UART(board.TX, board.RX, baudrate=9600)

# Initialize the DFPlayer Mini module
dfplayer = DFPlayerMini(uart)

# Example usage:
dfplayer.set_volume(15)  # Set volume to 15 (0 to 30)
dfplayer.play_track(1)  # Play track number 1
dfplayer.pause()  # Pause the track
dfplayer.start()  # Resume playing the track
```

For more details on available commands and parameters, please refer to the [DFPlayerMini Documentation](https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299).

## Available Methods

- `set_volume(volume)`: Set the volume of the DFPlayer Mini module.
- `volume_up()`: Increase the volume.
- `volume_down()`: Decrease the volume.
- `set_eq(eq)`: Set the equalizer mode.
- `set_output_device(device)`: Set the output device.
- `play_track(track)`: Play a specific track.
- `loop_track(track)`: Loop a specific track.
- `pause()`: Pause the currently playing track.
- `start()`: Start/resume playing the track.
- `play_folder_track(folder, track)`: Play a specific track in a folder.
- `enable_loop_all()`: Enable loop mode for all tracks.
- `disable_loop_all()`: Disable loop mode for all tracks.
- `play_mp3_track(track)`: Play a specific MP3 track.
- `advertise_track(track)`: Advertise a specific track.
- `stop_advertise()`: Stop advertising.
- `play_large_folder_track(folder, track)`: Play a specific track in a large folder.
- `loop_folder(folder)`: Loop all tracks in a specific folder.
- `random_all()`: Play all tracks in random order.
- `enable_loop()`: Enable loop mode for the current track.
- `disable_loop()`: Disable loop mode for the current track.
- `read_state()`: Read the current state of the DFPlayer Mini module.
- `read_volume()`: Read the current volume level.
- `read_eq()`: Read the current equalizer mode.
- `read_file_counts()`: Read the total number of files in the SD card.
- `read_current_file_number()`: Read the current file number being played.
- `read_file_counts_in_folder(folder)`: Read the total number of files in a specific folder.

For more details on available commands and parameters, please refer to the [DFPlayerMini Documentation](https://wiki.dfrobot.com/DFPlayer_Mini_SKU_DFR0299).

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contributions and Support

Contributions to this project are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

For support, contact joonas.joensuu[at]gmail[dot]com

## Acknowledgements

Special thanks to DFRobot for their DFPlayer Mini library and to OpenAI for the assistance provided by ChatGPT-3.5 during the porting process.

## Disclaimer

This project is provided as-is, without any warranty or support. Please use it at your own risk.
Please copy and paste the above content into your README.md file.

