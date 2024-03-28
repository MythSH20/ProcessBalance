import psutil
import torch

print(psutil.cpu_freq())
print(psutil.cpu_percent(percpu=True))
print(psutil.cpu_times())
print(psutil.cpu_times_percent())
print(psutil.cpu_stats())
print(psutil.cpu_count(logical=True))
print(psutil.virtual_memory())
print(psutil.swap_memory())
print(psutil.disk_usage('/'))
print(psutil.disk_io_counters())

# sysinfo = {
#     "cpu_frequency": cpu_frequency_tensor,
#     "cpu_percent": cpu_percent_tensor,
#     "cpu_times": cpu_times_tensor,
#     "cpu_time_percent": cpu_time_percent_tensor,
#     "cpu_stats": cpu_stats_tensor,
#     "cpu_count": cpu_count_tensor,
#     "memory_info": memory_info_tensor,
#     "swap_memory": swap_memory_tensor,
#     "disk_percent": disk_percent_tensor,
#     "io_counter": io_counter_tensor
# }

# 获取当前进程的 PID
# pid = 35516
#
# # 获取进程相关信息
# process = psutil.Process(pid)
#
# # 打印进程相关信息
# print(process.cpu_percent(interval=0.01))
# print(process.cpu_times())
# print(process.cpu_affinity())
# print(process.num_threads())
# print(process.io_counters())
# print(process.memory_percent())
# print(process.memory_info())
# print(len(process.open_files()))
#
# process.cpu_percent(interval=0.01)
# process.cpu_times().user
# process.cpu_times().system
# process.cpu_affinity()
# process.num_threads()
# process.io_counters().read_count
# process.io_counters().write_count
# process.io_counters().other_count
# process.io_counters().read_bytes
# process.io_counters().write_bytes
# process.io_counters().other_bytes
# process.memory_percent()
# process.memory_info().rss
# process.memory_info().vms
# process.memory_info().num_page_faults
# process.memory_info().peak_wset
# process.memory_info().wset
# process.memory_info().peak_paged_pool
# process.memory_info().paged_pool
# process.memory_info().peak_nonpaged_pool
# process.memory_info().nonpaged_pool
#
# len(process.open_files())

# rss (Resident Set Size): 实际物理内存占用量，即进程当前正在使用的物理内存的大小（以字节为单位）。
#
# vms (Virtual Memory Size): 虚拟内存大小，即进程当前地址空间的大小（以字节为单位）。虚拟内存是可用于进程的总内存大小，包括物理内存和交换空间。
#
# num_page_faults: 页面错误次数，表示从未在物理内存中的页面调入物理内存的次数。页面错误是由于内存访问导致的缺页异常。
#
# peak_wset (Peak Working Set Size): 工作集大小的峰值，即进程在其整个生命周期中所使用的物理内存的最大值（以字节为单位）。
#
# wset (Working Set Size): 工作集大小，即进程当前正在使用的物理内存的大小（以字节为单位）。与 RSS 相似，但可能包括共享内存。
#
# peak_paged_pool: 分页池的峰值大小，即进程所分配的分页池的最大值（以字节为单位）。分页池用于存储操作系统的数据结构和信息。
#
# paged_pool: 分页池大小，即进程当前所分配的分页池的大小（以字节为单位）。
#
# peak_nonpaged_pool: 非分页池的峰值大小，即进程所分配的非分页池的最大值（以字节为单位）。非分页池用于存储操作系统的数据结构和信息。
#
# nonpaged_pool: 非分页池大小，即进程当前所分配的非分页池的大小（以字节为单位）。
#
# pagefile: 页面文件大小，即进程的页面文件占用大小（以字节为单位）。页面文件是用作虚拟内存扩展的文件。
#
# peak_pagefile: 页面文件的峰值大小，即进程的页面文件的最大大小（以字节为单位）。
#
# private: 私有内存大小，即进程当前正在使用的私有内存的大小（以字节为单位）。私有内存是进程独占使用的内存，不与其他进程共享。
# import psutil
# import torch
#
# pid = 30500
# process = psutil.Process(pid)
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
# memory_percent_tensor = torch.tensor(state_info["memory_percent"])
# print("memory_info_tensor 大小:", memory_percent_tensor.size())
# print(memory_percent_tensor)
#
# # import subprocess
# # import os
# #
# #
# # def run(c_file):
# #     gcc_path = r"D:\IDE\mingw64\bin"  # 假设GCC的路径是C:\MinGW\bin
# #     os.environ['PATH'] += os.pathsep + gcc_path
# #     filename = os.path.splitext(os.path.basename(c_file))[0]
# #     # 构建编译命令
# #     command = f"gcc \"{c_file}\" -o \"{c_file[:-2]}.exe\""
# #     subprocess.Popen(command, shell=True)
# #     command = f"{c_file[:-2]}.exe"
# #     subprocess.Popen(command, shell=True)
# #
# #
# # if __name__ == '__main__':
# #     # c_file = "stress/fpu.c"
# #     file = "F:\WorkPlace\ProcessBA\stress\\fibonacci.c"
# #     run(file)
# #
# # # import os
# # # import subprocess
# # # import time
# # #
# # # import numpy as np
# # # import psutil
# # #
# # # from config import learning_rate, discount_factor, epsilon, num_cores, stress_folder
# # # # from stress import compile_and_execute_c_file
# # # from info import get_processes_info, get_system_info, get_all_processes
# # # from stress import get_c_files
# # #
# # # # c_file = "F:\Work Place\Python\ProcessBA_Linux\stress\\fpu.c"
# # # # '''windows下编译与执行'''
# # # # match = re.match(r'(.*)\.c', c_file)
# # # # execute_name = match.group(1) + ".exe"
# # # # command = 'gcc' + str(match) + ' .c -o executable'
# # # # compile_process = subprocess.Popen(command, shell=True)
# # # # execute_process = subprocess.Popen([execute_name])
# # #
# # # import os
# # # import subprocess
# # #
# # # # 设置环境变量
# # # os.environ["PATH"] = "/path/to/your/program:" + os.environ["PATH"]
# # #
# # # # 调用C程序的命令
# # # # command = "./stress/fpu.c"
# # # command = r"stress/fpu.c"
# # # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
# # #
# # # # 获取输出
# # # output, _ = process.communicate()
# # #
# # # # 打印输出
# # # print("Output:", output.decode())
# # #
# # # # # 启动C程序
# # # # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# # # #
# # # # # 获取输出
# # # # output, error = process.communicate()
# # #
# # # # 打印输出和错误
# # # # try:
# # # #     print("Output:", output.decode('utf-8'))
# # # # except UnicodeDecodeError:
# # # #     print("Output contains non-utf-8 characters")
# # # #
# # # # try:
# # # #     print("Error (decoded with GB2312):", error.decode('gb2312'))
# # # # except UnicodeDecodeError:
# # # #     print("Error contains non-gb2312 characters")
# # # #
# # # # try:
# # # #     print("Error (decoded with GBK):", error.decode('gbk'))
# # # # except UnicodeDecodeError:
# # # #     print("Error contains non-gbk characters")
# # #
# # # # '''1'''
# # # # with open(c_file, 'r', encoding='utf-8') as file:
# # # #     file_content = file.read()
# # # #     print(file_content)
