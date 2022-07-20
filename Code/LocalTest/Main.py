from flask import Flask
import sys

COUNTER, STEP = 0, 1
app = Flask(__name__)


@app.route('/trajectory')
def get_trajectory():
    global COUNTER, STEP
    info = lines[COUNTER]
    COUNTER += STEP
    if COUNTER == len(lines):
        STEP = -1
    if COUNTER == 0:
        STEP = 1
    return info


if __name__ == '__main__':
    limit = sys.argv[1]
    trajectory_log = open(f"trajectory_history_{limit}", "r")
    lines = trajectory_log.readlines()
    app.run()
