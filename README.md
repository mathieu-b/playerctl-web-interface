# Playerctl Web Interface for Linux

A minimalist web interface for controlling media playback of various media players using `playerctl`.

This project utilizes Flask to create a simple web server that allows users to play, pause, and navigate through media tracks. Audio volume is controlled via `amixer` since volume control does not work on certain Spotify (and maybe others too?).


## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd playerctl-web-interface
   ```

2. Install `uv`: https://docs.astral.sh/uv/getting-started/installation/


## Usage

1. Start the application:
   ```
   ./run.sh
   ```

2. Open your web browser and navigate to `http://localhost:5000` to access the interface.


## License

This project is licensed under the MIT License. See the LICENSE file for more details.