import subprocess
import time
import os
import psutil


# def compile_and_execute_c_file(c_file):
#     process_name = []
#     compile_time = []
#     execute_time = []
#     all_process = psutil.process_iter()
#     # 编译 C 文件
#
#     process_name.append(str(c_file))
#     start_compile_time = time.time()
#     # compile_process = subprocess.run(["gcc", c_file_path, "-o", "executable"])
#     compile_process = subprocess.Popen(["gcc", c_file, "-o", "executable"])
#     # compile_process = launch_c_program()
#     compile_pid = compile_process.pid  # 获取编译进程的 PID
#     action =
#     set_cpu_affinity(compile_pid, action)
#
#     # 等待编译进程结束
#     compile_process.wait()
#     end_compile_time = time.time()
#     compile_time.append(end_compile_time - start_compile_time)
#
#     # 获取编译进程的 CPU 使用率和内存使用率
#     compile_cpu_usage = psutil.Process(compile_pid).cpu_percent()
#     compile_memory_usage = psutil.Process(compile_pid).memory_percent()
#
#     # 执行生成的可执行文件
#     start_execute_time = time.time()
#     execute_process = subprocess.Popen(["./executable"])
#     execute_pid = execute_process.pid
#     set_cpu_affinity(execute_pid, affinity)
#
#     # 等待执行结束
#     execute_process.wait()
#     end_execute_time = time.time()
#     execute_time
#     return process_name, compile_time, execute_time


def get_c_files(directory):
    c_files = []
    # 遍历文件夹中的所有文件
    for filename in os.listdir(directory):
        # 检查文件是否是以 .c 结尾的 C 文件
        if filename.endswith(".c"):
            c_files.append(os.path.join(directory, filename))
    return c_files

# if __name__ == "__main__":
#     c_file_path = "your_c_file.c"  # 替换为你的 C 文件路径
#     compile_and_execute_c_file(c_file_path)
