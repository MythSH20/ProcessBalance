import subprocess
import os


def run(c_file):
    gcc_path = r"D:\IDE\mingw64\bin"  # 假设GCC的路径是C:\MinGW\bin
    os.environ['PATH'] += os.pathsep + gcc_path
    filename = os.path.splitext(os.path.basename(c_file))[0]
    # 构建编译命令
    command = f"gcc \"{c_file}\" -o \"{c_file[:-2]}.exe\""
    subprocess.Popen(command, shell=True)
    command = f"{c_file[:-2]}.exe"
    subprocess.Popen(command, shell=True)


if __name__ == '__main__':
    # c_file = "stress/fpu.c"
    file = "F:\WorkPlace\ProcessBA\stress\\fibonacci.c"
    run(file)

# import os
# import subprocess
# import time
#
# import numpy as np
# import psutil
#
# from config import learning_rate, discount_factor, epsilon, num_cores, stress_folder
# # from stress import compile_and_execute_c_file
# from info import get_processes_info, get_system_info, get_all_processes
# from stress import get_c_files
#
# # c_file = "F:\Work Place\Python\ProcessBA_Linux\stress\\fpu.c"
# # '''windows下编译与执行'''
# # match = re.match(r'(.*)\.c', c_file)
# # execute_name = match.group(1) + ".exe"
# # command = 'gcc' + str(match) + ' .c -o executable'
# # compile_process = subprocess.Popen(command, shell=True)
# # execute_process = subprocess.Popen([execute_name])
#
# import os
# import subprocess
#
# # 设置环境变量
# os.environ["PATH"] = "/path/to/your/program:" + os.environ["PATH"]
#
# # 调用C程序的命令
# # command = "./stress/fpu.c"
# command = r"stress/fpu.c"
# process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
#
# # 获取输出
# output, _ = process.communicate()
#
# # 打印输出
# print("Output:", output.decode())
#
# # # 启动C程序
# # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
# #
# # # 获取输出
# # output, error = process.communicate()
#
# # 打印输出和错误
# # try:
# #     print("Output:", output.decode('utf-8'))
# # except UnicodeDecodeError:
# #     print("Output contains non-utf-8 characters")
# #
# # try:
# #     print("Error (decoded with GB2312):", error.decode('gb2312'))
# # except UnicodeDecodeError:
# #     print("Error contains non-gb2312 characters")
# #
# # try:
# #     print("Error (decoded with GBK):", error.decode('gbk'))
# # except UnicodeDecodeError:
# #     print("Error contains non-gbk characters")
#
# # '''1'''
# # with open(c_file, 'r', encoding='utf-8') as file:
# #     file_content = file.read()
# #     print(file_content)
