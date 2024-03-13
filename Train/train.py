import psutil
# from stress import compile_and_execute_c_file
from multiprocessing import Pool
from functools import partial
from info import get_processes_info, get_system_info, get_all_processes
from config import learning_rate, discount_factor, epsilon, num_cores, stress_folder
from stress import get_c_files
from affinity import set_cpu_affinity
import time
import numpy as np
import subprocess
import threading
import multiprocessing


def run_process():
    start_time = time.time()
    # 在这里运行你的进程
    subprocess.run(["your_command_here"])
    end_time = time.time()
    return end_time - start_time


class ProcessBalance:
    def __init__(self, actions):
        # action取决于核心数量
        self.num_core = num_cores
        self.num_actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.q_table = np.zeros((self.num_core, self.num_actions))
        self.states = get_all_processes(True)

    def update_states(self):
        self.states = get_all_processes(True)

    def learn(self, state, action, reward, next_state, pids):
        get_processes_info(pids)
        now_q_value = self.q_table[state][action]
        new_q_value = reward + self.discount_factor * max(self.q_table[next_state])
        self.q_table[state][action] += self.learning_rate * (new_q_value - now_q_value)
        pass

    def update_reward(self, compile_time, execute_time):
        reward = 1 / (compile_time + execute_time)
        return reward

    def choose_action(self, state):
        if np.random.uniform(0, 1) < self.epsilon:
            # 探索：以 epsilon 的概率随机选择动作
            action = np.random.randint(self.num_actions)
        else:
            # 利用：选择具有最高Q值的动作
            q_values = self.q_table[state]
            action = np.argmax(q_values)
        return action

    # def start_process(self):
    #     c_files = get_c_files("stress")
    #     for file in c_files:
    #         affinity = self.choose_action()
    #         compile_and_execute_c_file(file, affinity)

    def compile_and_execute_c_file(self, c_file):
        process_name = []
        compile_time = []
        execute_time = []
        all_process = psutil.process_iter()
        # 编译 C 文件

        process_name.append(str(c_file))
        start_compile_time = time.time()
        # compile_process = subprocess.run(["gcc", c_file_path, "-o", "executable"])
        compile_process = subprocess.Popen(["gcc", c_file, "-o", "executable"])
        # compile_process = launch_c_program()
        compile_pid = compile_process.pid  # 获取编译进程的 PID
        action = self.choose_action(get_processes_info(compile_process))
        set_cpu_affinity(compile_pid, action)

        # 等待编译进程结束
        compile_process.wait()
        end_compile_time = time.time()
        compile_time.append(end_compile_time - start_compile_time)

        # 获取编译进程的 CPU 使用率和内存使用率
        compile_cpu_usage = psutil.Process(compile_pid).cpu_percent()
        compile_memory_usage = psutil.Process(compile_pid).memory_percent()

        # 执行生成的可执行文件
        start_execute_time = time.time()
        execute_process = subprocess.Popen(["./executable"])
        execute_pid = execute_process.pid
        action = self.choose_action(get_processes_info(compile_process))
        set_cpu_affinity(execute_pid, action)

        # 等待执行结束
        execute_process.wait()
        end_execute_time = time.time()
        execute_time = end_execute_time - start_execute_time
        return process_name, compile_time, execute_time

    def train(self, epochs):
        for epoch in range(epochs):
            system_info = get_system_info(True)
            c_files = get_c_files(stress_folder)
            with Pool() as pool:
                pool.map(self.compile_and_execute_c_file, c_files)
                pool.close()
                pool.join()


def predict():
    pass


# start process->get pid->choose action(affinity) by state->set affinity->return state->update q value
def main():
    epoc = 100
    actions = 4
    train_process = ProcessBalance(actions)
    train_process.train(epoc)


if __name__ == "__main__":
    main()
