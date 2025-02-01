#include "server.h"
#include <csignal>
#include <iostream>
#include <csignal>

volatile bool running = true;

void signalHandler(int signal) {
    running = false;
}

int main() {
    signal(SIGINT, signalHandler);

    Server server(8080);
    try {
        server.start(running);
    } catch (const std::exception& e) {
        std::cerr << "Server error: " << e.what() << std::endl;
        return EXIT_FAILURE;
    }

    std::cout << "Server shutting down..." << std::endl;
    return EXIT_SUCCESS;
}