import os
import re
import subprocess
import threading
import time
import platform
import random

import numpy as np
import psutil
import torch
import torch.nn as nn
import torch.optim as optim

from config import learning_rate, discount_factor, epsilon, num_cores, stress_folder, gcc_path
# from stress import compile_and_execute_c_file
from info import get_processes_info, get_system_info, get_all_processes
from stress import get_c_files
from affinity import set_cpu_affinity


# def run_process():
#     start_time = time.time()
#     # 在这里运行你的进程
#     subprocess.run(["your_command_here"])
#     end_time = time.time()
#     return end_time - start_time


class State:
    def __init__(self, cpu_percent, io_percent, memory_percent, process_affinities):
        self.cpu_percent = cpu_percent
        self.process_affinities = process_affinities
        self.io_percent = io_percent
        self.memory_percent = memory_percent


class Action:
    def __init__(self, core_num, core_efficiency):
        self.core_num = core_num
        self.core_efficiency = core_efficiency


def cal_reward(error_need_edit):
    pas = 114514
    return pas


class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        self.fc1 = nn.Linear(state_dim, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


state_dim = 11
action_dim = 8  # 8个核心
q_network = QNetwork(state_dim, action_dim)

criterion = nn.MSELoss()
optimizer = optim.Adam(q_network.parameters(), lr=0.001)


def choose_action(state):
    # 根据当前状态 state 和 Q-network q_network 计算每个动作的 Q 值
    q_values = q_network(state)

    # 根据 ε-greedy 策略选择动作
    if random.random() < epsilon:
        # 探索：随机选择一个动作
        action = random.randint(0, q_values.size(0) - 1)
    else:
        # 利用：选择具有最大 Q 值的动作
        action = torch.argmax(q_values).item()

    return action


def q_learning(state, action, reward, next_state, gamma=0.99):
    q_values = q_network(state)
    next_q_values = q_network(next_state)
    target = reward + gamma * torch.max(next_q_values)
    loss = criterion(q_values[action.core_index], target)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def compile_and_execute_c_file(c_file):
    process_name = []
    compile_time = []
    execute_time = []
    all_process = psutil.process_iter()
    os_type = platform.system()

    start_compile_time = time.time()

    '''windows下编译'''
    if os_type == "Windows":
        os.environ['PATH'] += os.pathsep + gcc_path
        filename = os.path.splitext(os.path.basename(c_file))[0]
        command = f"gcc \"{c_file}\" -o \"{c_file[:-2]}.exe\""
        compile_process = subprocess.Popen(command, shell=True)
        compile_pid = compile_process.pid
        # state = get_processes_info(compile_pid)
        # action = self.choose_action(state)
        # process_name = os.path.abspath(c_file)

        '''linux下编译'''
    elif os_type == "Linux":
        compile_process = subprocess.run(["gcc", c_file, "-o", "executable"])
        compile_pid = compile_process.pid
        action = choose_action(get_processes_info(compile_process))
        set_cpu_affinity(compile_pid, action)

    compile_process.wait()
    end_compile_time = time.time()

    '''windows下执行'''
    if os_type == "Windows":
        command = f"{c_file[:-2]}.exe"
        execute_process = subprocess.Popen(command)
        execute_pid = execute_process.pid
        execute_process_info = get_processes_info(execute_pid)
        action = choose_action(execute_process_info)
        reward = cal_reward()
        '''Q更新'''
        q_learning(execute_process_info, action, reward, compile_process)
        set_cpu_affinity(execute_pid, action)

        '''linux下执行'''
    # elif os_type == "Linux":
    #     # 执行
    #     start_execute_time = time.time()
    #     execute_process = subprocess.Popen(["./executable"])
    #     execute_pid = execute_process.pid
    #
    #     action = choose_action(get_processes_info(compile_process))
    #     set_cpu_affinity(execute_pid, action)
    #     process_info_execute = get_processes_info(execute_pid)
    #
    #     # 等待执行结束
    #     execute_process.wait()
    #     end_execute_time = time.time()
    #     execute_time = end_execute_time - start_execute_time

    compile_time = end_compile_time - start_compile_time

    # return process_name, compile_time, execute_time


def train(epochs):
    system_core_nums = 8
    system_core_efficiency = [1, 1, 1, 1, 0.8, 0.8, 0.8, 0.8]
    action = Action(system_core_nums, system_core_efficiency)

    # 初始化 Q 网络
    state_dim = ...  # 输入维度，根据状态的特征数确定
    action_dim = ...  # 输出维度，根据动作的数量确定
    q_network = QNetwork(state_dim, action_dim)

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.Adam(q_network.parameters(), lr=0.001)

    for epoch in range(epochs):
        system_info = get_system_info(True)
        c_files = get_c_files(stress_folder)
        threads = []
        # 多线程地启动
        start_time = time.time()
        for program in c_files:
            compile_and_execute_c_file(program)
            # thread = threading.Thread(target=self.compile_and_execute_c_file, args=(program))
            # thread.start()
            # threads.append(thread)


def predict():
    pass


# start process->get pid->choose action(affinity) by state->set affinity->return state->update q value
def main():
    epoc = 3
    actions = 32

    train(epoc)


if __name__ == "__main__":
    main()
