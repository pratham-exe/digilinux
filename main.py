import subprocess
import time


def get_current_hypr_clients() -> set:
    hyprctl_clients = set()

    output = subprocess.run(["hyprctl", "clients"], capture_output=True, text=True)
    initial_title = None

    for each_line in output.stdout.split("\n"):
        each_line = each_line.strip()
        if each_line.startswith("initialTitle:"):
            initial_title = each_line.split(":", 1)[1].strip()
            if initial_title:
                hyprctl_clients.add(initial_title)

    return hyprctl_clients


def update_digital_wellbeing_hash_map(digital_wellbeing: dict, current_digital_wellbeing: set) -> dict:
    for each_application in current_digital_wellbeing:
        if each_application not in digital_wellbeing:
            digital_wellbeing[each_application] = [time.time(), 0, True]

    for each_app in digital_wellbeing.keys():
        if each_app in current_digital_wellbeing:
            if not digital_wellbeing[each_app][2]:
                end_time = time.time()
                digital_wellbeing[each_app][1] += end_time - digital_wellbeing[each_app][0]
            digital_wellbeing[each_app][2] = False
        digital_wellbeing[each_app][0] = time.time()

    return digital_wellbeing


def resume_time_for_all_applications(digital_wellbeing: dict) -> dict:
    for each_application in digital_wellbeing.keys():
        digital_wellbeing[each_application][0] = time.time()

    return digital_wellbeing
