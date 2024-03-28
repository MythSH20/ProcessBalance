#include <pthread.h>
#include <stdio.h>

#define NUM_THREADS 4

void *task(void *arg) {
    int thread_id = *((int *)arg);
    printf("Thread %d is running\n", thread_id);
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
    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];
    int thread_args[NUM_THREADS];

    // 创建并启动线程
    for (int i = 0; i < NUM_THREADS; ++i) {
        thread_args[i] = i;
        pthread_create(&threads[i], NULL, task, (void *)&thread_args[i]);
    }

    // 等待所有线程结束
    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], NULL);
    }

    return 0;
}
