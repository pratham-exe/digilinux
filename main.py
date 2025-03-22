import subprocess
import os
import time


def get_current_running_processes() -> dict:
    output = subprocess.run(["ps", "-eo", "comm,args"], capture_output=True, text=True)

    process_hash_map = {}

    for each_output in output.stdout.split("\n"):
        arguments = each_output.split(maxsplit=1)
        if len(arguments) == 2:
            process_hash_map[arguments[0]] = arguments[1]

    return process_hash_map


def get_all_applications() -> dict:
    output = subprocess.run(["ls", "/usr/share/applications/"], capture_output=True, text=True)

    applications_dir_path = "/usr/share/applications/"
    applications_hash_map = {}

    for file in output.stdout.strip().split("\n"):
        file_full_path = os.path.join(applications_dir_path, file)
        with open(file_full_path, "r") as f:
            for each_line in f:
                if each_line.startswith("Exec="):
                    execution_path = each_line.split("=", 1)[1].strip().split()[0]
                    applications_hash_map[file[:-8]] = execution_path

    return applications_hash_map


def get_current_processes_applications(process_list: dict, applications_list: dict) -> set:
    process_application_list = set()

    for name, args in process_list.items():
        if name in applications_list.keys():
            process_application_list.add(name)
        else:
            for app_name, exec_path in applications_list.items():
                if exec_path in args:
                    process_application_list.add(app_name)
                    break

    return process_application_list


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
