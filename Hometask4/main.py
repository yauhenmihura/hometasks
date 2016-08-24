import configparser
import psutil
import datetime
import time
import json
import schedule

config = configparser.ConfigParser()
config.read('config.ini')
output = config.get('common', 'output')
interval = config.get('common', 'interval')
snapshot = 1


class Var(object):
    def __init__(self):
        self.cpu = psutil.cpu_percent()
        self.mem_usage = (psutil.Process().memory_percent() * 100).__round__(2)
        self.mem_virt = (psutil.virtual_memory()[3] / (1024**2)).__round__(2)
        self.disk_usage = \
            (psutil.disk_io_counters()[2] / (1024**2)).__round__(2)
        self.disk_io = \
            (psutil.disk_io_counters()[3] / (1024**2)).__round__(2)
        self.net_usage = \
            (psutil.net_io_counters()[0] / (1024**2)).__round__(2)


class Main(Var):
    def outtxt(self):
        global snapshot
        format = '%Y-%m-%d %H:%M:%S %Z'
        time = datetime.datetime.now()
        snaptime = datetime.datetime.strftime(time, format)
        f = open('output.txt', "a")
        f.write("Snapshot {0}:, Snapshot Time - {1}:\n".format(snapshot, snaptime))
        f.write("CPU: {0} %\n".format(self.cpu))
        f.write("Memory Usage: {0} Mb\n".format(self.mem_usage))
        f.write("Virtual Memory: {0} Mb\n".format(self.mem_virt))
        f.write("Disk Usage {0} Mb\n".format(self.disk_usage))
        f.write("Disk IO {0} Mb\n".format(self.disk_io))
        f.write("Network Information {0} MB\n".format(self.net_usage))
        f.write("\n")
        f.close()
        snapshot += 1

    def outjson(self):
        global snapshot
        format = '%Y-%m-%d %H:%M:%S %Z'
        time = datetime.datetime.now()
        snaptime = datetime.datetime.strftime(time, format)
        dict = {
            'CPU': str(self.cpu) + ' %',
            'Memory Usage': str(self.mem_usage) + " MB",
            'Virtual Memory': str(self.mem_virt) + " MB",
            'Disk Usage': str(self.disk_usage) + " MB",
            'Disk IO': str(self.disk_io) + " MB",
            'Network Information': str(self.net_usage) + " MB",
        }
        data = \
            ['SNAPSHOT ' + str(snapshot) + ": " + str(snaptime) + ": ", dict]
        with open("output.json", "a") as i:
            json.dump(data, i, indent=3, sort_keys=True)
        snapshot += 1


def stxt():
    x = Main()
    x.outtxt()


def sjson():
    x = Main()
    x.outjson()


if output == "txt":
    print(output + ' output in output.txt every ' + interval + ' seconds')
    schedule.every(int(interval)).seconds.do(stxt)
elif output == "json":
    print(output + ' output in output.json every ' + interval + ' seconds')
    schedule.every(int(interval)).seconds.do(sjson)
else:
    print("Uncorrect format in config.ini")
    quit()
while True:
    schedule.run_pending()
    time.sleep(5)
