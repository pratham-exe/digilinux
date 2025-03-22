# digilinux - Digital Wellbeing for Linux

A web based application that tracks and monitors the time spent on different applications running on a Linux system. This project is configured to run as a **systemd service**, making it seamless to manage and control.


## Features
- Tracks running applications and monitors time spent on each.
- Displays application usage on a Flask based dashboard.
- Easy to install and manage via systemd.


## Prerequisites
- Python3
- Virtual Environment
- Flask
- Creating a Systemd Sleep Hook
    1. Create a digilinux.sh file.
        ```
        sudo nano /lib/systemd/system-sleep/digilinux.sh
        ```

    2. Add the following content.

```
#!/bin/bash

if [ "$1" = "pre" ]; then
    nohup curl -m 5 -X GET http://127.0.0.1:5000/sleep >/dev/null 2>&1 &
elif [ "$1" = "post" ]; then
    nohup curl -m 5 -X GET http://127.0.0.1:5000/resume >/dev/null 2>&1 &
fi
```

    3. Make the script executable.
        ```
        sudo chmod +x /lib/systemd/system-sleep/digilinux.sh
        ```


## Installation
- Clone the repository, create a virtual environment and install Flask.
    ```
    git clone https://github.com/pratham-exe/digilinux.git
    cd digilinux
    python3 -m venv digital
    source digital/bin/activate
    pip install flask
    ```
- Execute the installation script.
    ```
    chmod +x install.sh
    ./install.sh
    ```


## Usage
After running the `install.sh` script, visit `http://127.0.0.1:5000` to view the dashboard and track your time.
