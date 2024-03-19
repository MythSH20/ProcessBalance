#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/select.h>

int main() {
    fd_set fds;
    struct timeval tv;
    int ret;

    // 设置标准输入文件描述符
    FD_ZERO(&fds);
    FD_SET(STDIN_FILENO, &fds);

    // 设置超时时间为 1 秒
    tv.tv_sec = 1;
    tv.tv_usec = 0;

    while (1) {
        // 等待标准输入上的事件
        ret = select(STDIN_FILENO + 1, &fds, NULL, NULL, &tv);
        if (ret == -1) {
            perror("select");
            exit(EXIT_FAILURE);
        } else if (ret > 0) {
            if (FD_ISSET(STDIN_FILENO, &fds)) {
                // 标准输入上有数据可读
                char buf[256];
                if (fgets(buf, sizeof(buf), stdin) != NULL) {
                    printf("Received input: %s", buf);
                }
            }
        } else {
            // 超时，执行空闲操作或进入睡眠状态
            // 在这个示例中，我们什么也不做，继续等待事件
        }
    }

    return 0;
}
