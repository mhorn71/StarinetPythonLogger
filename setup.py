__author__ = 'mark'
application_title = "StarinetPython3Logger"
main_python_file = "StarinetPython3Logger.py"

import sys
from cx_Freeze import setup, Executable

base = None

includes = ["crcmod"]

setup(
       name = application_title,
       version = "5.0.4",
       description = "Starinet Python3 6 Channel Data Logger for Beaglebone Black",
       options = {"build_exe" : {"includes" : includes }},
       executables = [Executable(main_python_file, base = base)])
