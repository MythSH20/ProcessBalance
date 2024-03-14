#include <stdio.h>
#include <time.h>

#define ITERATIONS 10000 // 迭代次数

void fpu_pressure_test() {
    double result = 0.0;
    for (int j = 0; j < ITERATIONS; j++){
        for (int i = 0; i < ITERATIONS; i++) {
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
            result += (double)i / (i + 1); // 执行一系列浮点数运算
            result += (double)i * (i + 1); // 执行一系列浮点数运算
        }
    }
}

int main() {
    clock_t start_time, end_time;
    double cpu_time_used;

    start_time = clock(); // 记录开始时间
    fpu_pressure_test(); // 执行 FPU 压力测试
    end_time = clock(); // 记录结束时间

    cpu_time_used = ((double) (end_time - start_time)) / CLOCKS_PER_SEC; // 计算 CPU 时间
    printf("FPU 压力测试完成，运行时间：%f 秒\n", cpu_time_used);

    return 0;
}
