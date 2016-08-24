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

p = psutil.Process()
cpu = psutil.cpu_percent()
mem_usage = (p.memory_percent() * 100).__round__(2)
mem_virt = (psutil.virtual_memory()[3] / 1024 / 1024).__round__(2)
disk_usage = (psutil.disk_io_counters()[2] / 1024 / 1024).__round__(2)
disk_io = (psutil.disk_io_counters()[3] / 1024 / 1024).__round__(2)
net_usage = (psutil.net_io_counters()[0] / 1024 / 1024).__round__(2)
snapshot = 1


def outtxt():
    '''Function for writing results in txt file'''
    global snapshot
    format = '%Y-%m-%d %H:%M:%S %Z'
    time = datetime.datetime.now()
    snaptime = datetime.datetime.strftime(time, format)
    f = open('output.txt', "a")
    f.write("Snapshot {0}:, Snapshot Time - {1}:\n".format(snapshot, snaptime))
    f.write("CPU: {0}\n".format(cpu))
    f.write("Memory Usage: {0} Mb\n".format(mem_usage))
    f.write("Virtual Memory: {0} Mb\n".format(mem_virt))
    f.write("Disk Usage {0} Mb\n".format(disk_usage))
    f.write("Disk IO {0} Mb\n".format(disk_io))
    f.write("Network Information {0} MB\n".format(net_usage))
    f.write("\n")
    f.close()
    snapshot += 1


def outjson():
    '''Function for writing results in json file'''
    global snapshot
    format = '%Y-%m-%d %H:%M:%S %Z'
    time = datetime.datetime.now()
    snaptime = datetime.datetime.strftime(time, format)
    dict = {
        'CPU': str(cpu) + ' %',
        'Memory Usage': str(mem_usage) + " MB",
        'Virtual Memory': str(mem_virt) + " MB",
        'Disk Usage': str(disk_usage) + " MB",
        'Disk IO': str(disk_io) + " MB",
        'Network Information': str(net_usage) + " MB",
    }
    data = ['SNAPSHOT ' + str(snapshot) + ": " + str(snaptime) + ": ", dict]
    with open("output.json", "a") as i:
        json.dump(data, i, indent=3, sort_keys=True)
    snapshot += 1


if output == "txt":
    print(output + ' output in output.txt every ' + interval + ' seconds')
    schedule.every(int(interval)).seconds.do(outtxt)
elif output == "json":
    print(output + ' output in output.json every ' + interval + ' seconds')
    schedule.every(int(interval)).seconds.do(outjson)
else:
    print("Uncorrect format in config.ini")
    quit()
while True:
    schedule.run_pending()
    time.sleep(5)
