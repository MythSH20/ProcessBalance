#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>

#define DIRECTORY "IOFile_Library"
#define NUM_FILES 100

void create_files() {
    char filename[20];
    FILE *fp;

    // 创建文件夹
    mkdir(DIRECTORY, 0777);

    // 创建文件并写入数据
    for (int i = 1; i <= NUM_FILES; i++) {
        sprintf(filename, "%s/%d.txt", DIRECTORY, i);
        fp = fopen(filename, "w");
        if (fp == NULL) {
            printf("Error creating file %s\n", filename);
            exit(1);
        }
        fprintf(fp, "%d\n", i);
        fclose(fp);
    }
}

void delete_directory() {
    char command[100];
    // 使用系统命令删除整个文件夹
    sprintf(command, "rm -rf %s", DIRECTORY);
    system(command);
}

int main() {
    // 创建文件并写入数据
    create_files();

    // 删除整个文件夹
    delete_directory();

    return 0;
}
