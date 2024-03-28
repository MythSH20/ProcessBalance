import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import random
import gym
import os
import psutil


class DQN(nn.Module):
    def __init__(self, state_dim, action_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(state_dim, 24)
        self.fc2 = nn.Linear(24, 24)
        self.fc3 = nn.Linear(24, action_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []

    def push(self, transition):
        self.memory.append(transition)
        if len(self.memory) > self.capacity:
            del self.memory[0]

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


# 设置CPU亲和性
def set_cpu_affinity(pid, cpu_core):
    p = psutil.Process(pid)
    p.cpu_affinity([cpu_core])


# 训练DQN
def train_dqn(env, dqn, memory, optimizer, episodes, batch_size, gamma, epsilon, epsilon_min, epsilon_decay):
    for episode in range(episodes):
        state = env.reset()
        state = torch.tensor(state, dtype=torch.float32)
        done = False
        total_reward = 0
        while not done:
            # 选择动作
            if np.random.rand() <= epsilon:
                action = env.action_space.sample()
            else:
                with torch.no_grad():
                    q_values = dqn(state)
                    action = torch.argmax(q_values).item()

            # 执行动作
            next_state, reward, done, _ = env.step(action)
            next_state = torch.tensor(next_state, dtype=torch.float32)
            total_reward += reward

            # 存储转换
            memory.push((state, action, reward, next_state, done))

            # 更新状态
            state = next_state

            # 从经验重放中学习
            if len(memory) > batch_size:
                batch = memory.sample(batch_size)
                state_batch, action_batch, reward_batch, next_state_batch, done_batch = zip(*batch)
                state_batch = torch.stack(state_batch)
                action_batch = torch.tensor(action_batch, dtype=torch.long)
                reward_batch = torch.tensor(reward_batch, dtype=torch.float32)
                next_state_batch = torch.stack(next_state_batch)
                done_batch = torch.tensor(done_batch, dtype=torch.uint8)

                q_values = dqn(state_batch)
                next_q_values = dqn(next_state_batch)
                max_next_q_values = torch.max(next_q_values, dim=1)[0]
                target_values = reward_batch + (1 - done_batch) * gamma * max_next_q_values

                q_value = q_values.gather(dim=1, index=action_batch.unsqueeze(dim=1)).squeeze()

                loss = nn.MSELoss()(q_value, target_values.detach())
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # 调整epsilon
        epsilon = max(epsilon_min, epsilon * epsilon_decay)

        # 打印结果
        print(f"Episode: {episode + 1}/{episodes}, Total Reward: {total_reward}")


# 设置环境和DQN参数
env = gym.make('CartPole-v1')
state_dim = env.observation_space.shape[0]
action_dim = env.action_space.n
dqn = DQN(state_dim, action_dim)
memory = ReplayMemory(capacity=10000)
optimizer = optim.Adam(dqn.parameters(), lr=0.001)

# 获取当前进程ID和CPU核心数量
pid = os.getpid()
num_cores = psutil.cpu_count()

# 设置CPU亲和性
cpu_core = 0  # 设置为0号CPU核心，你可以根据自己的需求设置
set_cpu_affinity(pid, cpu_core)

# 开始训练
train_dqn(env, dqn, memory, optimizer, episodes=1000, batch_size=32, gamma=0.99, epsilon=1.0, epsilon_min=0.01,
          epsilon_decay=0.995)
