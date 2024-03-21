#include <stdio.h>
#include <time.h>

// 递归实现斐波那契数列，返回第 n 项的值
double fibonacci(int n)
{
    if (n <= 1)
    {
        return n;
    }
    else
    {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

int main()
{
    int n = 20; // 计算斐波那契数列的第 n 项
    int times = 2;
    double result = 0.;
    // printf("Calculating Fibonacci sequence for term %d...\n", n);
    clock_t start_time = clock();
    for (int i = 0; i < times; i++)
    {
        n = 45;
        result = fibonacci(n);
    }
    clock_t end_time = clock();
    double execution_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("Function execution time: %.6f seconds\n", execution_time);
    printf("The %dth term of Fibonacci sequence is: %0.llf\n", n, result);
    return 0;
}
