from flask import Flask, jsonify
import json
import sys

sys.path.append(sys.path[0].replace("server", ""))
from config import server_port

app = Flask(__name__)


# Victim target API for bots
@app.route('/', methods=['GET', 'POST'])
def index():
    f = open('victim.txt')
    VICTIM = f.read()
    f.close()

    VICTIM = json.loads(VICTIM)
    return jsonify(VICTIM)


if __name__ == "__main__":
    app.run(port=server_port)
