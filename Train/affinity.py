import os
import subprocess
import psutil
import platform


def set_cpu_affinity(pid, action):
    """
    设置进程的亲和性
    """
    process = psutil.Process(pid)
    cpu_cores = [0, 1, 2, 3]
    logical_core_nums = psutil.cpu_count(logical=True)
    physical_core_nums = psutil.cpu_count(logical=False)
    if logical_core_nums != physical_core_nums & logical_core_nums != 2 * physical_core_nums:
        if logical_core_nums <= 12:
            if action == 0:
                cpu_cores = [0, 1, 2, 3]
            elif action == 1:
                cpu_cores = [4, 5, 6, 7]
            elif action == 2:
                cpu_cores = [8, 9, 10, 11]
            process.cpu_affinity(cpu_cores)
        elif logical_core_nums <= 20:
            # 设置 CPU 亲和性
            if action == 0:
                cpu_cores = [0, 1, 2, 3]
            elif action == 1:
                cpu_cores = [10, 11, 12, 13]
            elif action == 2:
                cpu_cores = [16, 17, 18, 19]
            process.cpu_affinity(cpu_cores)
        elif logical_core_nums <= 24:
            # 设置 CPU 亲和性
            if action == 0:
                cpu_cores = [0, 1, 2, 3]
            elif action == 1:
                cpu_cores = [14, 15, 16, 17]
            elif action == 2:
                cpu_cores = [18, 19, 20, 21]
            process.cpu_affinity(cpu_cores)
        else:
            # 设置 CPU 亲和性
            if action == 0:
                cpu_cores = [0, 1, 2, 3]
            elif action == 1:
                cpu_cores = [14, 15, 16, 17]
            elif action == 2:
                cpu_cores = [18, 19, 20, 21]
            process.cpu_affinity(cpu_cores)
    else:
        # 设置 CPU 亲和性
        if action == 0:
            cpu_cores = [0, 1, 2, 3]
        elif action == 1:
            cpu_cores = [4, 5, 6, 7]
        elif action == 2:
            cpu_cores = [8, 9, 10, 11]
        process.cpu_affinity(cpu_cores)
    return cpu_cores


def launch_c_program(c_program_path, cpu_cores):
    """
    启动 C 程序并设置亲和性
    """
    # 启动 C 程序
    c_program_process = subprocess.Popen([c_program_path])

    # 设置进程的亲和性
    set_cpu_affinity(c_program_process.pid, cpu_cores)

# # 指定要启动的 C 程序路径
# c_program_path = "./your_c_program"
#
# # 指定要设置的 CPU 核心
# cpu_cores = [0]  # 将进程绑定到第一个 CPU 核心上
#
# # 启动 C 程序并设置亲和性
# launch_c_program(c_program_path, cpu_cores)
