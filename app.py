import threading
import time
from threading import Lock

from flask import Flask, jsonify, render_template
from main import (
    get_current_hypr_clients,
    resume_time_for_all_applications,
    update_digital_wellbeing_hash_map,
)

app = Flask(__name__)

digital_wellbeing_hash_map = {}
sleep_mode = False
lock = Lock()


def update_digital_wellbeing_data():
    global digital_wellbeing_hash_map

    while True:
        if not sleep_mode:
            current_digital_wellbeing_list = get_current_hypr_clients()
            with lock:
                digital_wellbeing_hash_map = update_digital_wellbeing_hash_map(
                    digital_wellbeing_hash_map, current_digital_wellbeing_list
                )

            time.sleep(1)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/data")
def get_data_from_main():
    global digital_wellbeing_hash_map

    data = {}
    for k, v in digital_wellbeing_hash_map.items():
        data[k] = v[1]

    return jsonify(data)


@app.route("/sleep", methods=["POST"])
def pause_time():
    global sleep_mode
    if not sleep_mode:
        with lock:
            sleep_mode = True

    return "OK", 200


@app.route("/resume", methods=["POST"])
def resume_time():
    global sleep_mode, digital_wellbeing_hash_map
    if sleep_mode:
        with lock:
            resume_time_for_all_applications(digital_wellbeing_hash_map)
            sleep_mode = False

    return "OK", 200


if __name__ == "__main__":
    background_thread = threading.Thread(
        target=update_digital_wellbeing_data, daemon=True
    )
    background_thread.start()

    app.run()
