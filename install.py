import os
import json
import time
import subprocess
from datetime import datetime

"""
Pretty Little Package Installer - CyberJosie
https://github.com/CyberJosie/Pretty-Little-Package-Installer
"""

SEP = '====================='
APP_NAME = ''   # Enter the name of the app the dependencies are for.
APP_VERSION = ''    # Enter an app version or leave blank

# Write APT packages here
APT_PACKAGES = [
    # "python3-scapy"
]

# Write PIP packages here
PIP_PACKAGES = [
    # "numpy"
]

class Color:
    def __init__(self):
        self.reset = "\u001b[0m"
        self.red = "\u001b[31m"
        self.green = "\u001b[32m"
        self.yellow = "\u001b[33m"
        self.blue = "\u001b[34m"
        self.magenta = "\u001b[35m"
        self.cyan = "\u001b[36m"
        self.white = "\u001b[37m"


def execute(command):
    result = subprocess.run([command], stdout=subprocess.PIPE, shell=True)
    return str(result.stdout.decode())

def timestamp(self):
    today = datetime.now()
    timestamp = today.strftime("%H:%M:%S")
    return timestamp

def get_pip_list():
    return execute("pip3 list").split("\n")


def is_apt_installed(package_name):
    result = execute(f"dpkg -s {package_name}")
    if "Status: install ok installed" in result:
        return True
    else:
        return False

def is_pip_installed(pip_package_name):
    pip_list = get_pip_list()
    installed = False
    for line in pip_list:
        if pip_package_name in line:
            installed = True
    return installed


def check_dependencies():
    pip_list = get_pip_list()
    c = Color()
    apt_output = {}
    pip3_output = {}

    for apt_pkg in APT_PACKAGES:
        if not is_apt_installed(apt_pkg):
            apt_output[apt_pkg] = "No"
        else:
            apt_output[apt_pkg] = "Yes"
    
    for pip_pkg in PIP_PACKAGES:
        if is_pip_installed(pip_pkg):
            pip3_output[pip_pkg] = "Yes"
        else:
            pip3_output[pip_pkg] = "No"
    
    print(f'{SEP}\n {c.yellow}APT Package Status:{c.reset}\n{SEP}\n{json.dumps(apt_output, indent=2)}\n')
    print(f'{SEP}\n {c.yellow}PIP Package Satatus:{c.reset}\n{SEP}\n{json.dumps(pip3_output, indent=2)}\n')

    return apt_output, pip3_output

def install_missing_depenencies(apt_output, pip3_output):
    c = Color()
    for pkg in list(apt_output.keys()):
        if apt_output[pkg] != "Yes":
            print(f'{c.green}INFO:{c.reset} APT Package {c.cyan}{pkg}{c.reset} is not installed, installing now...')
            os.system(f"sudo apt-get install -y {pkg}")
            time.sleep(0.5)
            if is_apt_installed(pkg):
                print(f'{c.green}INFO:{c.reset} Successfully installed {c.cyan}{pkg}{c.reset}.')
            else:
                print(f'{c.red}ERROR:{c.reset} Failed to install apt package \"{c.cyan}{pkg}{c.reset}\".')
        else:
            print(f'{c.green}INFO:{c.reset} APT Package {c.cyan}{pkg}{c.reset} is already installed.')
    
    for pkg in list(pip3_output.keys()):
        if pip3_output[pkg] != "Yes":
            print(f'{c.green}INFO:{c.reset} PIP Package {c.cyan}{pkg}{c.reset} is not installed, installing now...')
            os.system(f"sudo python3 -m pip install {c.cyan}{pkg}{c.reset}")
            time.sleep(0.5)
            if is_pip_installed(pkg):
                print(f'{c.green}INFO:{c.reset} Successfully installed {c.cyan}{pkg}{c.reset}.')
            else:
                print(f'{c.red}ERROR:{c.reset} Failed to install pip package \"{c.cyan}{pkg}{c.reset}\".')
        else:
            print(f'{c.green}INFO:{c.reset} PIP Package {c.cyan}{pkg}{c.reset} is already installed.')

if __name__ == '__main__':
    c = Color()
    print(f'Installing {c.yellow}{APP_NAME} {c.magenta}{APP_VERSION}{c.reset}...')
    apt, pip = check_dependencies()

    if input(f'- Press {c.cyan}Enter{c.reset} to install missing dependencies...(or \'q\' to quit)') != 'q':
        install_missing_depenencies(apt, pip)