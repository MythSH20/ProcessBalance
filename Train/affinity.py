import os
import subprocess
import psutil


def set_cpu_affinity(pid, cpu_core):
    """
    设置进程的亲和性
    """
    process = psutil.Process(pid)
    process.cpu_affinity(cpu_core)


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
