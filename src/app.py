# Description: This is the main file of the application. It contains the Flask server that will serve the frontend and the backend of the application.
# requires: https://github.com/altdesktop/playerctl

from flask import Flask, render_template, jsonify, request
import subprocess
from urllib import parse
import re


app = Flask(__name__)


_PREVIOUS_VOLUME = None
_PLAYERCTLD_PROCESS = None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/play', methods=['GET'])
def play():
    print('play')
    subprocess.run(['playerctl', 'play'])
    return jsonify(success=True)

@app.route('/pause', methods=['GET'])
def pause():
    print('pause')
    subprocess.run(['playerctl', 'pause'])
    return jsonify(success=True)

@app.route('/next', methods=['GET'])
def next_track():
    print('next')
    subprocess.run(['playerctl', 'next'])
    return jsonify(success=True)

@app.route('/previous', methods=['GET'])
def previous_track():
    print('previous')
    subprocess.run(['playerctl', 'previous'])
    return jsonify(success=True)

@app.route('/status', methods=['GET'])
def status():
    print('status')
    result = subprocess.run(['playerctl', 'status'], capture_output=True, text=True)
    return jsonify(status=result.stdout.strip())

@app.route('/volume_up', methods=['GET'])
def volume_up():
    #print('volume_up')
    #subprocess.run(['playerctl', 'volume', '0.1+'])
    # Use amixer -q sset Master 3%+ instead of playerctl volume 0.1+
    subprocess.run(['amixer', '-q', 'sset', 'Master', '5%+'])
    return jsonify(success=True)

@app.route('/volume_down', methods=['GET'])
def volume_down():
    print('volume_down')
    #subprocess.run(['playerctl', 'volume', '0.1-'])
    subprocess.run(['amixer', '-q', 'sset', 'Master', '5%-'])
    return jsonify(success=True)

def get_amixer_master_volume_percent_string():
    # Example output to be parsed by this function ( from 'amixer sget Master')
    # Simple mixer control 'Master',0
    #  Capabilities: pvolume pswitch pswitch-joined
    #  Playback channels: Front Left - Front Right
    #  Limits: Playback 0 - 65536
    #  Mono:
    #  Front Left: Playback 32768 [50%] [on]
    #  Front Right: Playback 32768 [50%] [on]
    result = subprocess.run(['amixer', 'sget', 'Master'], capture_output=True, text=True)
    amixer_output = result.stdout.strip()
    # Parse the output using multi-line regex:
    matches = re.search(r'Front Left: Playback (\d+) \[(\d+)%\] \[on\]', amixer_output)
    if matches:
        return matches.group(2) + "%"
    else:
        return None


@app.route('/mute', methods=['GET'])
def mute():
    global _PREVIOUS_VOLUME
    print('mute')
    if _PREVIOUS_VOLUME:
        print("Restoring previous volume", _PREVIOUS_VOLUME)
        subprocess.run(['amixer', '-q', 'sset', 'Master', _PREVIOUS_VOLUME])
        _PREVIOUS_VOLUME = None
    else:
        # subprocess.run(['playerctl', 'volume', '0'])
        master_volume_percent = get_amixer_master_volume_percent_string()
        if master_volume_percent is not None:
            _PREVIOUS_VOLUME = master_volume_percent
            print("Saving previous volume", _PREVIOUS_VOLUME)
            subprocess.run(['amixer', '-q', 'sset', 'Master', '0'])

    return jsonify(success=True)

@app.route('/seek', methods=['GET'])
def seek():
    offset = parse.unquote(request.args.get('offset'))
    print('seek', offset)
    subprocess.run(['playerctl', 'position', str(offset)])
    return jsonify(success=True)


def check_prerequisites():
    try:
        subprocess.run(['playerctl', '--version'], capture_output=True, text=True)
    except FileNotFoundError:
        print('playerctl not found. Please install it before running this application.')
        exit(1)


def run_playerctld_in_background():
    global _PLAYERCTLD_PROCESS
    print('Starting playerctld process ...')
    _PLAYERCTLD_PROCESS = subprocess.Popen(['playerctld'])
    

# λ playerctl metadata
# spotify mpris:trackid             /com/spotify/track/0XIJQzbt0VCG3IFsj0TLsl
# spotify mpris:length              219627000
# spotify mpris:artUrl              https://i.scdn.co/image/ab67616d0000b2730bf52d404599796ba1d6e058
# spotify xesam:album               Quiet Stars
# spotify xesam:albumArtist         Advaitas
# spotify xesam:artist              Advaitas
# spotify xesam:autoRating          0.23000000000000001
# spotify xesam:discNumber          1
# spotify xesam:title               Om Mantra
# spotify xesam:trackNumber         12
# spotify xesam:url                 https://open.spotify.com/track/0XIJQzbt0VCG3IFsj0TLsl


def main():
    try:
        check_prerequisites()
        run_playerctld_in_background()
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        if _PLAYERCTLD_PROCESS:
            print('Killing playerctld process ...')
            _PLAYERCTLD_PROCESS.kill()


if __name__ == '__main__':
    main()

    