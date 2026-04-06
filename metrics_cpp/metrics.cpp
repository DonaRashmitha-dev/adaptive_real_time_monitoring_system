#include <iostream>
#include <cstdlib>
#include <ctime>
#include <windows.h>

int main() {
    srand(time(0));

    while (true) {
        int cpu = rand() % 100;
        int memory = rand() % 100;
        int latency = rand() % 500;

        std::cout << cpu << "," << memory << "," << latency << std::endl;

        Sleep(1000); // 1 second delay
    }
}