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


def get_core_info():
    core_nums = psutil.cpu_count(logical=True)

    return core_nums,


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

    #

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

        cpu_percent = process_tensor(torch.tensor(process.cpu_percent(interval=0.01)))
        cpu_user_time = process_tensor(torch.tensor(process.cpu_times().user))
        cpu_system_time = process_tensor(torch.tensor(process.cpu_times().system))
        cpu_affinity = process_tensor(torch.tensor(process.cpu_affinity()))
        num_threads = process_tensor(torch.tensor(process.num_threads()))
        io_read_count = process_tensor(torch.tensor(process.io_counters().read_count))
        io_write_count = process_tensor(torch.tensor(process.io_counters().write_count))
        io_other_count = process_tensor(torch.tensor(process.io_counters().other_count))
        io_read_bytes = process_tensor(torch.tensor(process.io_counters().read_bytes))
        io_write_bytes = process_tensor(torch.tensor(process.io_counters().write_bytes))
        io_other_bytes = process_tensor(torch.tensor(process.io_counters().other_bytes))
        memory_percent = process_tensor(torch.tensor(process.memory_percent()))
        memory_rss = process_tensor(torch.tensor(process.memory_info().rss))
        memory_vms = process_tensor(torch.tensor(process.memory_info().vms))
        memory_page_faults = process_tensor(torch.tensor(process.memory_info().num_page_faults))
        memory_peak_wset = process_tensor(torch.tensor(process.memory_info().peak_wset))
        memory_wset = process_tensor(torch.tensor(process.memory_info().wset))
        memory_peak_paged_pool = process_tensor(torch.tensor(process.memory_info().peak_paged_pool))
        memory_paged_pool = process_tensor(torch.tensor(process.memory_info().paged_pool))
        memory_peak_nonpaged_pool = process_tensor(torch.tensor(process.memory_info().peak_nonpaged_pool))
        memory_nonpaged_pool = process_tensor(torch.tensor(process.memory_info().nonpaged_pool))

        system_info = get_system_info(True)
        cpu_count_logical = psutil.cpu_count(logical=True)
        if len(cpu_affinity) < cpu_count_logical:
            # 计算需要补充的个数
            num_to_append = cpu_count_logical - len(cpu_affinity)
            # 创建要添加的值为-1的张量
            appended_tensor = torch.full((num_to_append,), -1, dtype=torch.int32)
            # 将新的张量与原始张量拼接起来
            cpu_affinity = torch.cat((cpu_affinity, appended_tensor))

        # 将所有张量连接成一个张量
        state = torch.cat([
            cpu_percent,
            cpu_user_time,
            cpu_system_time,
            cpu_affinity,
            num_threads,
            io_read_count,
            io_write_count,
            io_other_count,
            io_read_bytes,
            io_write_bytes,
            io_other_bytes,
            memory_percent,
            memory_rss,
            memory_vms,
            memory_page_faults,
            memory_peak_wset,
            memory_wset,
            memory_peak_paged_pool,
            memory_paged_pool,
            memory_peak_nonpaged_pool,
            memory_nonpaged_pool,
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
        state = get_state(process.pid)

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
