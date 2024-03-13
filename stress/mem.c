#include <stdio.h>
#include <stdlib.h>

#define NUM_BLOCKS 1000
#define BLOCK_SIZE 1024 * 1024 // 1 MB

int main() {
    void *blocks[NUM_BLOCKS];

    // 分配内存块
    for (int i = 0; i < NUM_BLOCKS; i++) {
        blocks[i] = malloc(BLOCK_SIZE);
        if (blocks[i] == NULL) {
            printf("内存分配失败！\n");
            // 释放之前分配的内存块
            for (int j = 0; j < i; j++) {
                free(blocks[j]);
            }
            return 1;
        }
        // 将内存块初始化为零
        memset(blocks[i], 0, BLOCK_SIZE);
    }

    // 释放内存块
    for (int i = 0; i < NUM_BLOCKS; i++) {
        free(blocks[i]);
    }

    printf("内存压力测试完成！\n");

    return 0;
}
