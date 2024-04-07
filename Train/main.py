import concurrent
import os
import re
import subprocess
import threading
import time
import platform
import random
import pandas as pd

import numpy as np
import psutil
import torch
import torch.nn as nn
import torch.optim as optim

from config import learning_rate, discount_factor, epsilon, num_cores, stress_folder, gcc_path
# from stress import compile_and_execute_c_file
from info import get_state, get_system_info, get_all_processes
from stress import get_c_files
from affinity import set_cpu_affinity


def cal_reward(execute_time):
    reward = 1 / execute_time
    return reward


class QNetwork(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(QNetwork, self).__init__()
        hid1_size = 128
        hid2_size = 128
        self.fc1 = nn.Linear(state_dim, hid1_size)
        # 定义第二层全连接层
        self.fc2 = nn.Linear(hid1_size, hid2_size)
        # 定义第三层全连接层，输入单元数目为隐藏层神经元数目hid2_size，输出单元数目为action的维度
        self.fc3 = nn.Linear(hid2_size, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        y = torch.relu(self.fc2(x))
        q_value = self.fc3(y)
        return q_value


ACTIONS = [0, 1, 2]
max_cores = 32

action_dim = 3  # 3簇核心

state_dim = 100

timing = {}
files = []
origin_execute_times = {}
final_execute_times = {}


def save_log(file, time_data, dictionary, module):
    file = file.split('\\')[-1]
    if module == 1:
        if file in dictionary:
            dictionary[file] += time_data
        else:
            dictionary[file] = time_data
    elif module == 2:
        if file in dictionary:
            # Check if the value is a list, if not, convert it to a list
            if not isinstance(dictionary[file], list):
                dictionary[file] = [dictionary[file]]
            # Append the time data to the list
            dictionary[file].append(time_data)
        else:
            # If index doesn't exist, create a new entry with the time value as a list
            dictionary[file] = [time_data]


def get_sys_dim():
    pid = os.getpid()
    state = get_state(pid)
    state_dim = state.size(0)
    return state_dim


q_network = QNetwork(get_sys_dim(), action_dim)

criterion = nn.MSELoss()
optimizer = optim.Adam(q_network.parameters(), lr=0.001)


# 根据当前状态 state 和 Q-network q_network 计算每个动作的 Q 值
def choose_action(state):
    # 根据当前状态 state 和 Q-network q_network 计算每个动作的 Q 值
    q_values = q_network(state)

    # 根据 ε-greedy 策略选择动作
    if random.random() < epsilon:
        # 探索：随机选择一个动作
        selected_action = random.choice(ACTIONS)  # 从动作空间中随机选择一个动作
    else:
        # 利用：选择具有最大 Q 值的动作
        _, max_index = torch.max(q_values, dim=0)
        selected_action = max_index.item()  # 获取具有最大 Q 值的动作的索引

    return selected_action


def q_learning(state, action, reward, next_state, gamma=0.99):
    q_values = q_network(state)
    next_q_values = q_network(next_state)
    target = reward + gamma * torch.max(next_q_values)
    # print(action)`
    loss = criterion(q_values[action], target)
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

        '''linux下编译'''
    elif os_type == "Linux":
        compile_process = subprocess.run(["gcc", c_file, "-o", "executable"])
        compile_pid = compile_process.pid
        action = choose_action(get_state(compile_process))
        set_cpu_affinity(compile_pid, action)

    compile_process.wait()
    end_compile_time = time.time()

    '''windows下执行'''
    if os_type == "Windows":
        command = f"{c_file[:-2]}.exe"
        start_time = time.time()
        execute_process = subprocess.Popen(command)
        execute_pid = execute_process.pid
        state1 = get_state(execute_pid)
        action = choose_action(state1)
        affinity = set_cpu_affinity(execute_pid, action)
        print(str(affinity))

        '''调整亲和性并等待结束 '''
        action = choose_action(state1)
        state1 = get_state(execute_pid)
        execute_process.wait()
        end_time = time.time()
        time1 = end_time - start_time

        start_time = time.time()
        execute_process = subprocess.Popen(command)
        execute_pid = execute_process.pid
        affinity = set_cpu_affinity(execute_pid, action)
        print(str(affinity))
        execute_pid = execute_process.pid
        state2 = get_state(execute_pid)
        execute_process.wait()
        end_time = time.time()
        time2 = end_time - start_time

        '''Q更新'''
        time_ = time1 - time2
        save_log(c_file, time_, timing, 1)
        save_log(c_file, time1, origin_execute_times, 2)
        save_log(c_file, time2, final_execute_times, 2)

        reward = cal_reward(time_)
        q_learning(state1, action, reward, state2)

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


def train(epochs, num_threads):
    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = optim.Adam(q_network.parameters(), lr=0.001)

    for epoch in range(epochs):
        system_info = get_system_info(True)
        c_files = get_c_files(stress_folder)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            # 提交编译和执行任务
            futures = [executor.submit(compile_and_execute_c_file, c_file) for c_file in c_files]

            # 等待所有任务完成
            concurrent.futures.wait(futures)
    torch.save(q_network.state_dict(), '../model/q_network.pth')


def little_stress(epoc, num_threads):
    train(epoc, num_threads)
    print("训练轮次:" + str(epoc))
    print("线程数:" + str(num_threads))
    print(timing)

    average_time = {}
    for filename, times in origin_execute_times.items():
        average_time[filename] = sum(times) / len(times)
    print("origin_execute_times_average:" + str(average_time))

    for filename, times in final_execute_times.items():
        average_time[filename] = sum(times) / len(times)
    print("final_execute_times_average:" + str(average_time))
    print(origin_execute_times)
    print(final_execute_times)
    pass


def large_stress(epoc, num_threads):
    pass


# start process->get pid->choose action(affinity) by state->set affinity->return state->update q value
def main():
    epoc = 50
    num_threads = 12

    little_stress(epoc, num_threads)


if __name__ == "__main__":
    main()
