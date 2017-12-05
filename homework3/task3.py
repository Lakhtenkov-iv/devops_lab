'''Script stores following characteristics in file in format and interval defined in config.conf
Timestamp
Overall CPU load
Overall memory usage
Overall virtual memory usage
IO information
Network information
'''

import ConfigParser
from datetime import datetime
import json
import os.path
from time import sleep
import psutil

if not os.path.exists('config.conf'):
    print "Config file doesn't exist"
    quit()

config = ConfigParser.RawConfigParser()
config.read('config.conf')
COMMON_OUTPUT = config.get('common', 'output')
COMMON_INTERVAL = config.get('common', 'interval')
OUTPUT_FILE_NAME = 'output.' + COMMON_OUTPUT


def health_values_txt():
    '''Function returns string with system health parameters'''
    return '{timestamp} : CPU - {cpu:5}%, MEM - {mem:5}%, VIRTMEM - {vmem:5}%, \
    Disk i- {diskin}kB o- {diskout}kB, Net i- {netin}kB o- {netout}kB.'.format( \
                timestamp=datetime.now(), \
                cpu=sum(psutil.cpu_percent(interval=1, percpu=True)), \
                mem=psutil.virtual_memory().percent + psutil.swap_memory().percent, \
                vmem=psutil.virtual_memory().percent, \
                diskin=psutil.disk_io_counters(perdisk=False).write_count/1024, \
                diskout=psutil.disk_io_counters(perdisk=False).read_count/1024, \
                netin=psutil.net_io_counters().bytes_recv/1024, \
                netout=psutil.net_io_counters().bytes_sent/1024)


def health_values_json():
    '''Function returns json with system health parameters'''
    data = {
        'CPU': str(sum(psutil.cpu_percent(interval=1, percpu=True))),
        'MEM': str(psutil.virtual_memory().percent + psutil.swap_memory().percent),
        'VIRTMEM': str(psutil.virtual_memory().percent),
        'DiskInput': str(psutil.disk_io_counters(perdisk=False).write_count / 1024),
        'DiskOutput': str(psutil.disk_io_counters(perdisk=False).read_count / 1024),
        'NetInput': str(psutil.net_io_counters().bytes_recv / 1024),
        'NetOutput': str(psutil.net_io_counters().bytes_sent / 1024)
    }
    return json.dumps({str(datetime.now()): [data]}, \
                      sort_keys=False, separators=(', ', ': '))


if COMMON_OUTPUT == 'txt':

    while True:
        file = open(OUTPUT_FILE_NAME, 'a')
        file.write(health_values_txt()+"\n")
        file.close()
        sleep(float(COMMON_INTERVAL)*60)

elif COMMON_OUTPUT == 'json':

    while True:
        file = open(OUTPUT_FILE_NAME, 'a')
        file.write(health_values_json()+"\n")
        file.close()
        sleep(float(COMMON_INTERVAL)*60)
