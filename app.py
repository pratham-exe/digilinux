from flask import Flask, render_template, jsonify
from main import get_current_running_processes, get_all_applications, get_current_processes_applications, update_digital_wellbeing_hash_map
import time
import threading

app = Flask(__name__)

digital_wellbeing_hash_map = {}


def update_digital_wellbeing_data():
    global digital_wellbeing_hash_map

    while True:
        running_process_list = get_current_running_processes()
        present_applications_list = get_all_applications()

        current_digital_wellbeing_list = get_current_processes_applications(running_process_list, present_applications_list)
        digital_wellbeing_hash_map = update_digital_wellbeing_hash_map(digital_wellbeing_hash_map, current_digital_wellbeing_list)

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


if __name__ == "__main__":
    background_thread = threading.Thread(target=update_digital_wellbeing_data, daemon=True)
    background_thread.start()

    app.run()
