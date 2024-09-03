import os
import subprocess

output = subprocess.check_output("wmic process where \"caption='mstsc.exe' and commandline like '%{}.rdp%'\" get commandline, processid".format(item), shell=True)