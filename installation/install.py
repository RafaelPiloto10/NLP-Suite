"""
Install script for NLP Suite
https://github.com/NLP-Suite/NLP-Suite

A Natural Language Processing Bundle for social scientists
and non-professionals.

To learn more about how to install or run this file, visit:
https://github.com/NLP-Suite/NLP-Suite/wiki/Installation
"""

import os
import subprocess
import sys

NLP_SITE = "https://github.com/NLP-Suite/NLP-Suite/wiki/Support"

MAC = ["darwin"]
WINDOWS = ["win32 cygwin"]
LINUX = ["linux"]
AIX = ["aix"]

SUPPORTED_OS = [MAC, WINDOWS]


def get_consent(message: str) -> bool:
    put = input(f"[ATTENTION] {message} - [Y|N]: ")
    while not (put.lower() == "n" or put.lower() == "y" or put.lower() == "no" or put.lower() == "yes"):
        put = input("[ERROR] Invalid input. Please type 'Y' or 'N' (Yes|No, or Ctrl-C to quit): ")

    return put.lower() == "y" or put.lower() == "yes"



if __name__ == "__main__":

    OS = sys.platform # Get the user's OS
    if OS not in SUPPORTED_OS:
        print("[WARNING] Your operating system is not officially supported..")
        print("Your operating system will be treated as a unix system.")
        if not get_consent("Would you like to continue with the installation?"):
            print("Thank you for choosing NLP Suite!")
            exit(0)

    if OS in MAC:
        # Warn about Apple Silicon incompatibility
        print("[WARNING] If your Mac has the Apple Silicon Chip (M1), your operating system is not officially supported. Native support is not yet avaiable - please install using Rossetta.")

        print(f"[WARNING] Installation may run into errors or bugs. Please visit {NLP_SITE} for support and troubleshooting.")
        if not get_consent("Would you like to continue with your installation?"):
            print("Thank you for choosing NLP Suite!")
            exit(0)

        # Begin installation - Phase 1: XCode tools
        print("[INFO] Installing XCode tools.. please accept the following prompts to install the neccessary XCode tools.")
        print("[WARNING] This may take some time, please ensure you address any prompts to complete the installation")
        xcode_install = subprocess.run(["xcode-select", "--install"], capture_output = True)

        # Phase 2: Conda
        CONDA_PATH = subprocess.run("where conda".split(" "), capture_output = True)
        activate_conda = subprocess.run(["source", CONDA_PATH], capture_output = True)
        conda_init = subprocess.run("conda init".split(" "), capture_output = True)
        conda_init_zsh = subprocess.run("conda init zsh".split(" "), capture_output = True)

        print("[INFO] Installing HomeBrew...")
        brew_install = subprocess.run('echo | ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" brew install git'.split(" "), capture_output = True)

        if xcode_install.returncode != 0:
            print(f"[ERROR] There was an error installing xcode tools.. Got error:\n{xcode_install.stderr}")
            exit()
        
        if CONDA_PATH.returncode != 0:
            print(f"[ERROR] Could not locate conda.. Ensure you have Anaconda installed! Got error:\n{CONDA_PATH.stderr}")
            exit()
        if activate_conda.returncode != 0:
            print(f"[ERROR] ")
