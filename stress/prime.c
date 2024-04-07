#include <stdio.h>
#include <stdbool.h>
#include <time.h>

// 函数原型声明
bool isPrime(int number);

int main()
{
    int range = 50000000; // 指定范围
    int maxPrime = 2;     // 初始化为2，因为2是最小的素数
    clock_t start, end;
    double cpu_time_used;

    // 记录开始时间
    start = clock();

    // 从3开始遍历到指定范围
    for (int i = 3; i <= range; i++)
    {
        if (isPrime(i))
        {
            maxPrime = i; // 更新最大素数
        }
    }

    // 记录结束时间
    end = clock();

    // 输出最大素数
    printf("在范围内 %d 中最大的素数是: %d\n", range, maxPrime);

    // 计算执行时间
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("%d素数计算时间: %f 秒\n", range, cpu_time_used);

    return 0;
}

// 函数定义：判断一个数是否为素数
bool isPrime(int number)
{
    // 2是最小的素数
    if (number == 2)
    {
        return true;
    }
    // 排除偶数
    if (number % 2 == 0)
    {
        return false;
    }
    // 从3开始遍历到根号number，判断是否存在因子
    for (int i = 3; i * i <= number; i += 2)
    {
        if (number % i == 0)
        {
            return false;
        }
    }
    return true;
}
