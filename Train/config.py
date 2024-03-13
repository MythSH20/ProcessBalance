# 定义 Q-learning 参数
import os

learning_rate = 0.1  # 学习率
discount_factor = 0.9  # 折扣因子
epsilon = 0.1  # 探索率

# status
actions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

data_folder = os.path.join(os.path.dirname(__file__), '..', 'data')
num_cores = 4
save_folder = "save"
stress_folder = os.path.join(os.path.dirname(__file__), '..', 'stress')
