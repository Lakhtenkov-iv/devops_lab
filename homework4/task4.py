"""Script stores following characteristics in file in format and interval defined in config.conf
Timestamp
Overall CPU load
Overall memory usage
Overall virtual memory usage
IO information
Network information
"""

import ConfigParser
from datetime import datetime
import os.path
from time import sleep
import systemhealth


if not os.path.exists('config.conf'):
    print "Config file doesn't exist"
    quit()

config = ConfigParser.RawConfigParser()
config.read('config.conf')
common_output = config.get('common', 'output')
common_interval = config.get('common', 'interval')
output_file_name = 'output.' + common_output

current = systemhealth.System_health(datetime.now())

while True:
    file = open(output_file_name, 'a')
    if common_output == 'json':
        file.write(current.json() + "\n")
    elif common_output == 'txt':
        file.write(current.text() + "\n")
    file.close()
    sleep(float(common_interval)*60)
