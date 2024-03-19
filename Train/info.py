import os.path

import psutil
import json
import datetime
from config import data_folder, save_folder
import datetime


# class SystemInfo:
#     def __init__(self):
#         pass
#
#     def get_cpu_percent(self):
#         return psutil.cpu_percent()
#
#     def get_memory_percent(self):
#         return psutil.virtual_memory().percent
#
#     def get_all_info(self):
#         return 1


def get_system_info(is_save):
    # systeminfo = SystemInfo()
    cpu_frequency = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(percpu=True)
    cpu_times = psutil.cpu_times()

    cpu_time_percent = psutil.cpu_times_percent()
    cpu_stats = psutil.cpu_stats()

    memory_info = psutil.virtual_memory().percent
    swap_memory = psutil.swap_memory()

    # print("Total Memory:", memory_info.total)
    # print("Available Memory:", memory_info.available)
    # print("Used Memory:", memory_info.used)
    # print("Free Memory:", memory_info.free)
    # print("Memory Percent:", memory_info.percent)
    disk_percent = psutil.disk_usage('/')
    # print("Read Count:", disk_info.read_count)
    # print("Write Count:", disk_info.write_count)
    # print("Read Bytes:", disk_info.read_bytes)
    # print("Write Bytes:", disk_info.write_bytes)
    io_counter = psutil.disk_io_counters()

    sysinfo = {
        # cpu
        "cpu_frequency": cpu_frequency,
        "cpu_percent": cpu_percent,
        "cpu_time_percent": cpu_time_percent,
        "cpu_times": cpu_times,
        "cpu_stats": cpu_stats,

        # '''memory'''
        "memory_info": memory_info,
        "swap_memory ": swap_memory,

        # disk
        "disk_percent": disk_percent,

        # IO
        "io_counter": io_counter
    }
    system_info = json.dumps(sysinfo)
    if is_save:
        save_to_txt(save_folder, system_info)
    return sysinfo


# def get_processes_info(pids):
#     process_info = []
#     all_processes = []
#     for process in psutil.process_iter():
#         try:
#             p_name = process.name
#             p_id = process.pid
#             p_cpu = process.cpu_percent()
#             p_io = process.io_counters()
#             p_status = process.is_running()
#             p_time = psutil.boot_time()
#
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#
#     return

def get_pid(process_name):
    pass


# def get_processes_info(pids):
#     processes_info = []
#     for pid in pids:
#         try:
#             # 根据 PID 获取进程对象
#             psutil.pid_exists(pid)
#             process = psutil.Process(pid)
#
#             info = {
#                 "pid": pid,
#                 "name": process.name(),
#                 "status": process.status(),
#                 "cpu_percent": process.cpu_percent(),
#                 "io": process.io_counters(),
#                 "memory_percent": process.memory_percent(),
#
#             }
#             processes_info.append(info)
#         except psutil.NoSuchProcess:
#             # 如果进程不存在，则忽略该进程
#             print("ERROR:No such process:" + pid)
#             pass
#     return processes_info

def get_processes_info(pid):
    state = {}
    try:
        # 根据 PID 获取进程对象
        psutil.pid_exists(pid)
        process = psutil.Process(pid)
        info = {
            "pid": process.pid,
            "name": process.name(),
            "status": process.status(),
            "cpu_percent": process.cpu_percent(interval=0.01),
            "cpu_time": process.cpu_times(),
            "cpu_affinity": process.cpu_affinity(),
            "threads": process.num_threads(),
            "io": process.io_counters(),
            "memory_percent": process.memory_percent(),
            "memory_info": process.memory_info(),
            "num_fileDescriptors": process.num_fds()
        }
        state = {
            info["pid"],
            info["name"],
            info["status"],
            info["cpu_percent"],
            info["cpu_time"],
            info["cpu_affinity"],
            info["threads"],
            info["io"],
            info["memory_percent"],
            info["memory_info"],
            info["num_fileDescriptors"]
        }
        # state = pid, process.name(), process.status(), process.cpu_percent(
        #     interval=1), process.io_counters(), process.memory_percent()
        # info = {
        #     "pid": pid,
        #     "name": process.name(),
        #     "status": process.status(),
        #     "cpu_percent": process.cpu_percent(interval=1),
        #     "io": process.io_counters(),
        #     "memory_percent": process.memory_percent(),
        # }
    except psutil.NoSuchProcess:
        # 如果进程不存在，则忽略该进程
        print("ERROR:No such process:" + str(pid))
        pass
    return state


def get_all_processes(is_save):
    states = {}
    all_processes = list(psutil.process_iter())
    for process in all_processes:
        info = {
            "pid": process.pid,
            "name": process.name(),
            "status": process.status(),
            "cpu_percent": process.cpu_percent(interval=0.0001),
            "cpu_time": process.cpu_times(),
            "cpu_affinity": process.cpu_affinity(),
            "threads": process.num_threads(),
            "io": process.io_counters(),
            "memory_percent": process.memory_percent(),
            "memory_info": process.memory_info(),
            "num_fileDescriptors": process.num_fds()
        }
        state = {
            info["pid"],
            info["name"],
            info["status"],
            info["cpu_percent"],
            info["cpu_time"],
            info["cpu_affinity"],
            info["threads"],
            info["io"],
            info["memory_percent"],
            info["memory_info"],
            info["num_fileDescriptors"]
        }
        states[process.pid] = state
    if is_save:
        save_process(all_processes)
    return states


def save_process(all_processes):
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data_{timestamp}.json"  # 可以根据需要修改文件名的前缀和后缀
    # if not os.path.exists(filename):
    #     data = {"example_key": "example_value", "timestamp": str(datetime.datetime.now())}
    #     # 将数据写入文件
    if not os.path.exists("data"):
        os.mkdir("data")
    with open(os.path.join(data_folder, filename), 'w+') as f:
        f.write(str(all_processes) + '\n')


def save_to_txt(folder, data):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")  # 格式化时间为年-月-日_小时-分钟-秒
    file_path = folder + '\\' + formatted_time + '.txt'
    with open(file_path, 'w+') as file:
        file.write(data)


#
# def get_SysandProcessInfo():
#     get_processes_info(True)

if __name__ == '__main__':
    pid = 3376
    get_processes_info(pid)
    i = 0
    i += 1
