import configparser, psutil, datetime, time, json, schedule

config = configparser.ConfigParser()
config.read('config.ini')
output = config.get('common', 'output')
interval = config.get('common', 'interval')

p=psutil.Process()
cpu = psutil.cpu_percent(percpu=True)
mem_usage=(p.memory_percent()*100).__round__(2)
mem_virt = psutil.virtual_memory()
disk_usage = psutil.disk_usage('/')
disk_io = psutil.disk_io_counters()
net_usage = psutil.net_io_counters(pernic=True)
snapshot = 1

def outtxt():
    '''Function for writing results in txt file'''
    global snapshot
    format = '%Y-%m-%d %H:%M:%S %Z'
    time = datetime.datetime.now()
    snaptime = datetime.datetime.strftime(time, format)
    f = open('output.txt', "a")
    f.write("Snapshot {0}:, Snapshot Time - {1}:\n".format(snapshot, snaptime))
    f.write("CPU: {0}\n".format(cpu[0]))
    f.write("Memory Usage: {0} Mb\n".format(mem_usage))
    f.write("Virtual Memory: {0} Mb\n".format(mem_virt[0] / 1048576))
    f.write("Disk Usage {} Mb\n".format(disk_usage[0] / 1048576))
    f.write("Disk IO {0} Mb\n".format(disk_io[0] / 1048576))
    f.write("Network Information {}\n".format(net_usage))
    f.write("\n")
    f.close()
    snapshot += 1

def dictionary(js):
    """Create dictionary"""
    value = list(js)
    key = js._fields
    result = dict(zip(key, value))
    return result

def outjson():
    '''Function for writing results in json file'''
    global snapshot
    format = '%Y-%m-%d %H:%M:%S %Z'
    time = datetime.datetime.now()
    snaptime = datetime.datetime.strftime(time, format)
    jsonf = open("output.json", "a")
    jsonf.write("\nSnapshot #{0}, Snapshot Time - {1}\n".format(snapshot, snaptime))
    jsonf.write("\nCPU\n")
    json.dump(cpu_load, jsonf, indent=1)
    jsonf.write("\nMemory Usage\n")
    json.dump(mem_usage, jsonf, indent=1)
    jsonf.write("\nVirtual Memory\n")
    json.dump(dictionary(mem_virt), jsonf, indent=1)
    jsonf.write("\nDisk Usage\n")
    json.dump(dictionary(disk_usage), jsonf, indent=1)
    jsonf.write("\nDisk IO\n")
    json.dump(dictionary(disk_io), jsonf, indent=1)
    jsonf.write("\nNetwork Information\n")
    json.dump(net_usage, jsonf, indent=1)
    jsonf.write("\n\n")
    jsonf.close()
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