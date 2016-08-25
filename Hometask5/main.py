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
dec = config.getboolean('common', 'dec')
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

    def mydec(log):
        def inner(*args, **kwargs):
            l = open('myapp.log', "a")
            l.write('Start\nSnapshot:{}\n'.format(snapshot))
            l.write('Function name:{0},{1},{2}\n'.format(log.__name__, args, kwargs))
            log(*args, **kwargs)
            l.write('Stop\n')
            l.write('\n')
            l.close()
        return inner if dec else log

class Main(Var):

    @Var.mydec
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


    @Var.mydec
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

@Var.mydec
def start():
    if output == "txt":
        x = Main()
        x.outtxt()
        print(output + ' output in output.txt every ' + interval + ' seconds')
    elif output == "json":
        x = Main()
        x.outjson()

schedule.every(int(interval)).seconds.do(start)
while True:
    schedule.run_pending()
