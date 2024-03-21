import os
import subprocess
import psutil


def set_cpu_affinity(pid, actions):
    """
    设置进程的亲和性
    """
    # 提取 CPU 核心列表
    core_list = [action.core_num for action in actions]

    # 将核心列表转换为整数列表
    cpu_affinity = [core for core_list in core_list for core in core_list]

    # 设置 CPU 亲和性
    process = psutil.Process(os.getpid())
    process.cpu_affinity(cpu_affinity)


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
