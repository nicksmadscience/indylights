from flask import Flask, render_template, send_from_directory
import socket

# from lightthingy2 import *

app = Flask(__name__)

# lt = LightThingy("config.yaml", 1, 1, "10.0.0.100")

# temp
ch = [0] * 512
port = 6454
physical = 1
universe = 1


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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

sock.sendto(channels, ("10.0.0.205", port))





@app.route('/assets/<path:path>')
def send_asset(path):
    return send_from_directory('assets', path)

@app.route("/")
def index():
    return render_template("index.html")





if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5007)