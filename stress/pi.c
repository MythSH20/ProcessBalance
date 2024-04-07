#include <stdio.h>
#include <time.h>

double calculate_pi(int iterations)
{
    double pi = 0.0;
    int sign = 1;
    for (int i = 0; i < iterations; i++)
    {
        pi += sign * 4.0 / (2 * i + 1);
        sign *= -1; // 切换正负号
    }
    return pi;
}

int main()
{
    clock_t start, end;
    double cpu_time_used;

    int i = 0;
    double pi = 0.;
    long long int iterations = 500000; // 迭代次数，越大结果越精确

    start = clock(); // 记录开始时间

    for (i = 0; i <= 5000; i++)
    {
        pi = calculate_pi(iterations);
    }

    end = clock(); // 记录结束时间

    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC; // 计算执行时间，单位为秒

    printf("计算得到的圆周率（迭代次数 %d）：%.10f\n", iterations, pi);
    printf("圆周率运行时间: %f seconds\n", cpu_time_used);

    return 0;
}
