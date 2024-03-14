#include <stdio.h>

int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

int main() {
    int n = 10000; // 要计算的斐波那契数列项数
    for (int i = 0; i < n; i++) {
        //printf("%d ", fibonacci(i));
    }
    return 0;
}
