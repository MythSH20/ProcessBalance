import os.path

import psutil
import json
import datetime

import torch

from config import data_folder, save_folder
import datetime


def process_tensor(tensor):
    if tensor.dim() == 0:
        tensor = tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）
    return tensor


def get_system_info(is_save):
    cpu_frequency = psutil.cpu_freq()
    cpu_percent = psutil.cpu_percent(percpu=True)
    cpu_times = psutil.cpu_times()
    cpu_time_percent = psutil.cpu_times_percent()
    cpu_stats = psutil.cpu_stats()
    cpu_count = psutil.cpu_count(logical=True)

    memory_info = psutil.virtual_memory()
    swap_memory = psutil.swap_memory()

    disk_percent = psutil.disk_usage('/')
    io_counter = psutil.disk_io_counters()

    # cpu_frequency = torch.tensor(psutil.cpu_freq(), dtype=torch.float32)
    # cpu_percent = torch.tensor(psutil.cpu_percent(percpu=True))
    # cpu_times = torch.tensor(psutil.cpu_times())
    # cpu_time_percent = torch.tensor(psutil.cpu_times_percent())
    # cpu_stats = torch.tensor(psutil.cpu_stats())
    # cpu_count = torch.tensor(psutil.cpu_count(logical=True))
    #
    # memory_info = torch.tensor(psutil.virtual_memory())
    # swap_memory = torch.tensor(psutil.swap_memory())
    #
    # disk_percent = torch.tensor(psutil.disk_usage('/'))
    # io_counter = torch.tensor(psutil.disk_io_counters())

    sysinfo = {
        "cpu_frequency": cpu_frequency,
        "cpu_percent": cpu_percent,
        "cpu_times": cpu_times,
        "cpu_time_percent": cpu_time_percent,
        "cpu_stats": cpu_stats,
        "cpu_count": cpu_count,
        "memory_info": memory_info,
        "swap_memory": swap_memory,
        "disk_percent": disk_percent,
        "io_counter": io_counter
    }
    # for key, value in sysinfo.items():
    #     if isinstance(value, (int, float)):
    #         sysinfo[key] = torch.tensor(value, dtype=torch.float32)  # 转换标量为张量
    #     elif isinstance(value, dict):
    #         sysinfo[key] = torch.tensor(list(value.values()), dtype=torch.float32)  # 转换字典值为张量
    #     elif isinstance(value, list):
    #         sysinfo[key] = torch.tensor(value, dtype=torch.float32)  # 转换列表为张量

    cpu_frequency = torch.tensor(sysinfo["cpu_frequency"])
    cpu_percent = torch.tensor(sysinfo["cpu_percent"])
    cpu_times = torch.tensor(sysinfo["cpu_times"])
    cpu_time_percent = torch.tensor(sysinfo["cpu_time_percent"])
    cpu_stats = torch.tensor(sysinfo["cpu_stats"])
    cpu_count = torch.tensor(sysinfo["cpu_count"])
    memory_info = torch.tensor(sysinfo["memory_info"])
    swap_memory = torch.tensor(sysinfo["swap_memory"])
    disk_percent = torch.tensor(sysinfo["disk_percent"])
    io_counter = torch.tensor(sysinfo["io_counter"])

    sysinfo = torch.cat([
        cpu_frequency,
        cpu_percent,
        cpu_times,
        cpu_time_percent,
        cpu_stats,
        cpu_count,
        memory_info,
        swap_memory,
        disk_percent,
        io_counter])

    return sysinfo
    # # systeminfo = SystemInfo()
    # cpu_frequency = psutil.cpu_freq()
    # cpu_percent = psutil.cpu_percent(percpu=True)
    # cpu_times = psutil.cpu_times()
    #
    # cpu_time_percent = psutil.cpu_times_percent()
    # cpu_stats = psutil.cpu_stats()
    #
    # memory_info = psutil.virtual_memory().percent
    # swap_memory = psutil.swap_memory()
    #
    # # print("Total Memory:", memory_info.total)
    # # print("Available Memory:", memory_info.available)
    # # print("Used Memory:", memory_info.used)
    # # print("Free Memory:", memory_info.free)
    # # print("Memory Percent:", memory_info.percent)
    # disk_percent = psutil.disk_usage('/')
    # # print("Read Count:", disk_info.read_count)
    # # print("Write Count:", disk_info.write_count)
    # # print("Read Bytes:", disk_info.read_bytes)
    # # print("Write Bytes:", disk_info.write_bytes)
    # io_counter = psutil.disk_io_counters()
    #
    # sysinfo = {
    #     # cpu
    #     "cpu_frequency": cpu_frequency,
    #     "cpu_percent": cpu_percent,
    #     "cpu_time_percent": cpu_time_percent,
    #     "cpu_times": cpu_times,
    #     "cpu_stats": cpu_stats,
    #
    #     # '''memory'''
    #     "memory_info": memory_info,
    #     "swap_memory ": swap_memory,
    #
    #     # disk
    #     "disk_percent": disk_percent,
    #
    #     # IO
    #     "io_counter": io_counter
    # }
    # system_info = json.dumps(sysinfo)
    # if is_save:
    #     save_to_txt(save_folder, system_info)
    # return sysinfo


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

def get_state(pid):
    state = {}
    info = {}
    try:
        # 根据 PID 获取进程对象
        psutil.pid_exists(pid)
        process = psutil.Process(pid)

        # 将字典中的信息转换为张量
        cpu_percent_tensor = torch.tensor(process.cpu_percent(interval=0.01))
        cpu_time_tensor = torch.tensor(process.cpu_times())
        cpu_affinity_tensor = torch.tensor(process.cpu_affinity())
        threads_tensor = torch.tensor(process.num_threads())
        io_tensor = torch.tensor(process.io_counters())
        memory_percent_tensor = torch.tensor(process.memory_percent())
        memory_info_tensor = torch.tensor(process.memory_info())
        num_file_descriptors_tensor = torch.tensor(len(process.open_files()))

        # state_info = {
        #     "cpu_percent": process.cpu_percent(interval=0.01),
        #     "cpu_time": process.cpu_times(),
        #     "cpu_affinity": process.cpu_affinity(),
        #     "threads": process.num_threads(),
        #     "io": process.io_counters(),
        #     "memory_percent": process.memory_percent(),
        #     "memory_info": process.memory_info(),
        #     "num_fileDescriptors": len(process.open_files())
        # }
        #
        # # 将字典中的信息转换为张量
        # cpu_percent_tensor = torch.tensor(state_info["cpu_percent"])
        # cpu_time_tensor = torch.tensor(state_info["cpu_time"])
        # cpu_affinity_tensor = torch.tensor(state_info["cpu_affinity"])
        # threads_tensor = torch.tensor(state_info["threads"])
        # io_tensor = torch.tensor(state_info["io"])
        # memory_percent_tensor = torch.tensor(state_info["memory_percent"])
        # memory_info_tensor = torch.tensor(state_info["memory_info"])
        # num_file_descriptors_tensor = torch.tensor(state_info["num_fileDescriptors"])

        # 检查并处理 cpu_percent_tensor
        if cpu_percent_tensor.dim() == 0:
            cpu_percent_tensor = cpu_percent_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 cpu_time_tensor
        if cpu_time_tensor.dim() == 0:
            cpu_time_tensor = cpu_time_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 cpu_affinity_tensor
        if cpu_affinity_tensor.dim() == 0:
            cpu_affinity_tensor = cpu_affinity_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 threads_tensor
        if threads_tensor.dim() == 0:
            threads_tensor = threads_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 io_tensor
        if io_tensor.dim() == 0:
            io_tensor = io_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 memory_info_tensor
        if memory_info_tensor.dim() == 0:
            memory_info_tensor = memory_info_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 num_file_descriptors_tensor
        if num_file_descriptors_tensor.dim() == 0:
            num_file_descriptors_tensor = num_file_descriptors_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        system_info = get_system_info(True)
        if len(state_info["cpu_affinity"]) < psutil.cpu_count(logical=True):
            state_info["cpu_affinity"] += [-1] * (psutil.cpu_count(logical=True) - len(state_info["cpu_affinity"]))

        # 将所有张量连接成一个张量
        state = torch.cat([
            cpu_percent_tensor,
            cpu_time_tensor,
            cpu_affinity_tensor,
            threads_tensor,
            io_tensor,
            memory_percent_tensor,
            memory_info_tensor,
            num_file_descriptors_tensor,
            system_info
        ])

    except psutil.NoSuchProcess:
        # 如果进程不存在，则忽略该进程
        print("ERROR:No such process:" + str(pid))
        pass
    return state


def get_all_processes(is_save):
    states = {}
    all_processes = list(psutil.process_iter())
    for process in all_processes:
        state_info = {
            "cpu_percent": process.cpu_percent(interval=0.01),
            "cpu_time": process.cpu_times(),
            "cpu_affinity": process.cpu_affinity(),
            "threads": process.num_threads(),
            "io": process.io_counters(),
            "memory_percent": process.memory_percent(),
            "memory_info": process.memory_info(),
            "num_fileDescriptors": len(process.open_files())
        }

        # 将字典中的信息转换为张量
        cpu_percent_tensor = torch.tensor(state_info["cpu_percent"])
        cpu_time_tensor = torch.tensor(state_info["cpu_time"])
        cpu_affinity_tensor = torch.tensor(state_info["cpu_affinity"])
        threads_tensor = torch.tensor(state_info["threads"])
        io_tensor = torch.tensor(state_info["io"])
        memory_percent_tensor = torch.tensor(state_info["memory_percent"])
        memory_info_tensor = torch.tensor(state_info["memory_info"])
        num_file_descriptors_tensor = torch.tensor(state_info["num_fileDescriptors"])

        # 检查并处理 cpu_percent_tensor
        if cpu_percent_tensor.dim() == 0:
            cpu_percent_tensor = cpu_percent_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 cpu_time_tensor
        if cpu_time_tensor.dim() == 0:
            cpu_time_tensor = cpu_time_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 cpu_affinity_tensor
        if cpu_affinity_tensor.dim() == 0:
            cpu_affinity_tensor = cpu_affinity_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 threads_tensor
        if threads_tensor.dim() == 0:
            threads_tensor = threads_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 io_tensor
        if io_tensor.dim() == 0:
            io_tensor = io_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 memory_info_tensor
        if memory_info_tensor.dim() == 0:
            memory_info_tensor = memory_info_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 检查并处理 num_file_descriptors_tensor
        if num_file_descriptors_tensor.dim() == 0:
            num_file_descriptors_tensor = num_file_descriptors_tensor.unsqueeze(0)  # 将零维张量转换为一维张量（标量）

        # 将所有张量连接成一个张量
        state = torch.cat([
            cpu_percent_tensor,
            cpu_time_tensor,
            cpu_affinity_tensor,
            threads_tensor,
            io_tensor,
            # memory_percent_tensor,
            memory_info_tensor,
            num_file_descriptors_tensor
        ])

        # info = {
        #     "pid": process.pid,
        #     "name": process.name(),
        #     "status": process.status(),
        #     "cpu_percent": torch.tensor(process.cpu_percent(interval=0.01)),
        #     "cpu_time": torch.tensor(process.cpu_times()),
        #     "cpu_affinity": torch.tensor(process.cpu_affinity()),
        #     "threads": torch.tensor(process.num_threads()),
        #     "io": torch.tensor(process.io_counters()),
        #     "memory_percent": torch.tensor(process.memory_percent()),
        #     "memory_info": torch.tensor(process.memory_info()),
        #     "num_fileDescriptors": torch.tensor(len(process.open_files()))
        # }
        # state = torch.cat({
        #     info["cpu_percent"],
        #     info["cpu_time"],
        #     info["cpu_affinity"],
        #     info["threads"],
        #     info["io"],
        #     info["memory_percent"],
        #     info["memory_info"],
        #     info["num_fileDescriptors"]
        # })
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
    get_state(pid)
    i = 0
    i += 1
