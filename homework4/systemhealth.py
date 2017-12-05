"""
Module with System_health class defenition
"""

import json
import psutil

class System_health:
    """
    This is the class that contanes system characteristics as attributes
    """
    def __init__(self, timestamp):
        ''' Constructor'''
        self.timestamp = timestamp
        self.cpu = sum(psutil.cpu_percent(interval=1, percpu=True))
        self.mem = psutil.virtual_memory().percent + psutil.swap_memory().percent
        self.vmem = psutil.virtual_memory().percent
        self.diskin = psutil.disk_io_counters(perdisk=False).write_count/1024
        self.diskout = psutil.disk_io_counters(perdisk=False).read_count/1024
        self.netin = psutil.net_io_counters().bytes_recv/1024
        self.netout = psutil.net_io_counters().bytes_sent/1024


    def text(self):
        """This method returns current system health status in text format """
        return '{timestamp} : CPU - {cpu:5}%, MEM - {mem:5}%, VIRTMEM - {vmem:5}%, ' \
               'Disk i- {diskin}kB o- {diskout}kB, Net i- {netin}kB o- {netout}kB.'.format(
            timestamp=self.timestamp,
            cpu=self.cpu,
            mem=self.mem,
            vmem=self.vmem,
            diskin=self.diskin,
            diskout=self.diskout,
            netin=self.netin,
            netout=self.netout)

    def json(self):
        """This method returns current system health status in json format"""
        data = {}
        data.update({"CPU": self.cpu})
        data.update({"MEM": self.mem})
        data.update({"VMEM": self.vmem})
        data.update({"diskin": self.diskin})
        data.update({"diskout": self.diskout})
        data.update({"diskout": self.diskout})
        data.update({"netin": self.netin})
        data.update({"netout": self.netout})
        return json.dumps({str(self.timestamp): [data]})
