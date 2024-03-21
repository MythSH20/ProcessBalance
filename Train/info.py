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
    cpu_frequency_tensor = process_tensor(torch.tensor(psutil.cpu_freq()))
    cpu_percent_tensor = process_tensor(torch.tensor(psutil.cpu_percent(percpu=True)))
    cpu_times_tensor = process_tensor(torch.tensor(psutil.cpu_times()))
    cpu_time_percent_tensor = process_tensor(torch.tensor(psutil.cpu_times_percent()))
    cpu_stats_tensor = process_tensor(torch.tensor(psutil.cpu_stats()))
    cpu_count_tensor = process_tensor(torch.tensor(psutil.cpu_count(logical=True)))

    memory_info_tensor = process_tensor(torch.tensor(psutil.virtual_memory()))
    swap_memory_tensor = process_tensor(torch.tensor(psutil.swap_memory()))

    disk_percent_tensor = process_tensor(torch.tensor(psutil.disk_usage('/')))
    io_counter_tensor = process_tensor(torch.tensor(psutil.disk_io_counters()))

    sysinfo = {
        "cpu_frequency": cpu_frequency_tensor,
        "cpu_percent": cpu_percent_tensor,
        "cpu_times": cpu_times_tensor,
        "cpu_time_percent": cpu_time_percent_tensor,
        "cpu_stats": cpu_stats_tensor,
        "cpu_count": cpu_count_tensor,
        "memory_info": memory_info_tensor,
        "swap_memory": swap_memory_tensor,
        "disk_percent": disk_percent_tensor,
        "io_counter": io_counter_tensor
    }

    sysinfo = torch.cat([
        cpu_frequency_tensor,
        cpu_percent_tensor,
        cpu_times_tensor,
        cpu_time_percent_tensor,
        cpu_stats_tensor,
        cpu_count_tensor,
        memory_info_tensor,
        swap_memory_tensor,
        disk_percent_tensor,
        io_counter_tensor])

    return sysinfo


def get_state(process_pid):
    state = {}
    try:
        # 根据 PID 获取进程对象
        psutil.pid_exists(process_pid)
        process = psutil.Process(process_pid)

        # 将字典中的信息转换为张量
        cpu_percent_tensor = process_tensor(torch.tensor(process.cpu_percent(interval=0.01)))
        cpu_time_tensor = process_tensor(torch.tensor(process.cpu_times()))
        cpu_affinity_tensor = process_tensor(torch.tensor(process.cpu_affinity()))
        threads_tensor = process_tensor(torch.tensor(process.num_threads()))
        io_tensor = process_tensor(torch.tensor(process.io_counters()))
        memory_percent_tensor = process_tensor(torch.tensor(process.memory_percent()))
        memory_info_tensor = process_tensor(torch.tensor(process.memory_info()))
        num_file_descriptors_tensor = process_tensor(torch.tensor(len(process.open_files())))

        system_info = get_system_info(True)
        cpu_count_logical = psutil.cpu_count(logical=True)
        if len(cpu_affinity_tensor) < cpu_count_logical:
            # 计算需要补充的个数
            num_to_append = cpu_count_logical - len(cpu_affinity_tensor)
            # 创建要添加的值为-1的张量
            appended_tensor = torch.full((num_to_append,), -1, dtype=torch.int32)
            # 将新的张量与原始张量拼接起来
            cpu_affinity_tensor = torch.cat((cpu_affinity_tensor, appended_tensor))

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
        print("ERROR:No such process:" + str(process_pid))
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

        # 将所有张量连接成一个张量
        state = torch.cat([
            cpu_percent_tensor,
            cpu_time_tensor,
            cpu_affinity_tensor,
            threads_tensor,
            io_tensor,
            memory_percent_tensor,
            memory_info_tensor,
            num_file_descriptors_tensor
        ])

        states[process.pid] = state
    if is_save:
        save_process(all_processes)
    return states


def save_process(all_processes):
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data_{timestamp}.json"  # 可以根据需要修改文件名的前缀和后缀
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


if __name__ == '__main__':
    pid = 3376
    get_state(pid)
    i = 0
    i += 1
