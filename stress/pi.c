#include <stdio.h>

double calculate_pi(int iterations) {
    double pi = 0.0;
    int sign = 1;
    for (int i = 0; i < iterations; i++) {
        pi += sign * 4.0 / (2 * i + 1);
        sign *= -1; // 切换正负号
    }
    return pi;
}

int main() {
    int iterations = 1000000; // 迭代次数，越大结果越精确
    double pi = calculate_pi(iterations);
    //printf("计算得到的圆周率（迭代次数 %d）：%.10f\n", iterations, pi);
    return 0;
}
