from flask import Flask, render_template, send_from_directory, request
import socket
import yaml

# from lightthingy2 import *

app = Flask(__name__)

# lt = LightThingy("config.yaml", 1, 1, "10.0.0.100")

# temp

def openyaml(path):
    with open(path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None

chans = [0] * 512

def sendArtNet(ch):
    port = 6454
    physical = 1
    universe = 1


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    channelString = ''
    for channel in ch:
        channelString += str(chr(channel))
    header = "Art-Net" + chr(0)   # 1 - ID
    header += chr(0) + "P"        # 2 - OpCode
    header += chr(0)              # 3 - ProtVerHi
    header += chr(14)             # 4 - ProtVerLo
    header += chr(0)              # 5 - Sequence
    header += chr(physical)      # 6 - Physical
    header += chr(universe)      # 7 - SubUni
    header += chr(0)              # 8 - Net
    header += chr(2) + chr(0)     # 9 - Length

    channels = bytearray()
    channels.extend(map(ord, header + channelString))

    sock.sendto(channels, ("255.255.255.255", port))





@app.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory('assets', path)


@app.route("/")
def index():
    scenes = openyaml("test.yaml")

    if "s" in request.args:
        s = request.args["s"]

        if s not in scenes:
            return "scene not found"
        else:
            if scenes[s]:
                for channel, value in scenes[s].items():
                    chans[channel] = value

            sendArtNet(chans)
            


        
    return render_template("scenes.html", scenes=scenes)





if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5007)