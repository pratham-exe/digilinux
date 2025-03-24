from flask import Flask, render_template, jsonify
from main import get_current_running_processes, get_all_applications, get_current_processes_applications, update_digital_wellbeing_hash_map, resume_time_for_all_applications
import time
import threading
from threading import Lock

app = Flask(__name__)

digital_wellbeing_hash_map = {}
sleep_mode = False
sleep_reset_hash_map = None
lock = Lock()


def update_digital_wellbeing_data():
    global digital_wellbeing_hash_map

    while True:
        if not sleep_mode:
            running_process_list = get_current_running_processes()
            present_applications_list = get_all_applications()

            current_digital_wellbeing_list = get_current_processes_applications(running_process_list, present_applications_list)
            with lock:
                digital_wellbeing_hash_map = update_digital_wellbeing_hash_map(digital_wellbeing_hash_map, current_digital_wellbeing_list)

            time.sleep(1)


def reset_hash_map_at_midnight():
    global digital_wellbeing_hash_map

    while True:
        current_time = time.localtime()
        if current_time.tm_hour == 0 and current_time.tm_min == 0:
            with lock:
                digital_wellbeing_hash_map.clear()

        time.sleep(60)


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
    global sleep_mode, sleep_reset_hash_map
    if not sleep_mode:
        with lock:
            sleep_mode = True
            sleep_reset_hash_map = time.localtime()

    return "OK", 200


@app.route("/resume", methods=["POST"])
def resume_time():
    global sleep_mode, sleep_reset_hash_map
    if sleep_mode:
        with lock:
            resume_time_for_all_applications(digital_wellbeing_hash_map)
            sleep_mode = False
            if sleep_reset_hash_map is not None and sleep_reset_hash_map.tm_mday != time.localtime().tm_mday:
                digital_wellbeing_hash_map.clear()
                sleep_reset_hash_map = None

    return "OK", 200


if __name__ == "__main__":
    background_thread = threading.Thread(target=update_digital_wellbeing_data, daemon=True)
    background_thread.start()

    reset_hash_map_thread = threading.Thread(target=reset_hash_map_at_midnight, daemon=True)
    reset_hash_map_thread.start()

    app.run()
