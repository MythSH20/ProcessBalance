#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>

#define MEMORY_SIZE (1024ULL * 1024 * 100) // 内存块大小，这里设为100MB，注意使用ULL避免溢出
#define NUM_ACCESS 30000                   // 内存访问次数，调整为较小的值

int main()
{
    clock_t start, end;
    double cpu_time_used;

    uint8_t *memory_block = (uint8_t *)malloc(MEMORY_SIZE); // 分配内存块
    if (memory_block == NULL)
    {
        printf("Failed to allocate memory.\n");
        return 1;
    }

    printf("Memory allocated successfully.\n");

    // 填充内存块
    for (size_t i = 0; i < MEMORY_SIZE; i++)
    {
        memory_block[i] = (uint8_t)(i % 256); // 将每个字节设置为0-255之间的值
    }

    printf("Memory filled with data.\n");

    // 设置随机种子
    srand(time(NULL));

    start = clock(); // 记录开始时间

    // 循环访问内存地址
    for (int i = 0; i < NUM_ACCESS; i++)
    {
        for (int j = 0; j < NUM_ACCESS; j++)
        {
            // 生成随机地址
            size_t index = rand() % MEMORY_SIZE;
            // 读取并写入内存，模拟内存访问
            memory_block[index] = memory_block[index];
        }
    }

    end = clock(); // 记录结束时间

    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC; // 计算执行时间，单位为秒

    printf("Memory access complete.\n");
    printf("内存压力测试时间: %f seconds\n", cpu_time_used);

    free(memory_block); // 释放内存块

    // printf("Memory freed.\n");

    return 0;
}
