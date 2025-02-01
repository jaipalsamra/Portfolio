#ifndef SERVER_H
#define SERVER_H

#include "ThreadPool.h"
#include "HttpRequest.h"
#include "HttpResponse.h"
#include <netinet/in.h>
#include <string>

class Server {
private:
    int port;
    int serverSocket;
    ThreadPool threadPool;

    void handleClient(int clientSocket);
    void handleWebSocketHandshake(HttpRequest& request, int clientSocket);

    // 1) WebSocket loop for reading and responding to frames
    void handleWebSocket(int clientSocket);

    // 2) Helper to receive frames
    std::string receiveFrame(int clientSocket, bool &connectionOpen, unsigned char &opcode);

    // 3) Helper to send frames
    void sendFrame(int clientSocket, const std::string &message, unsigned char opcode = 0x1);

public:
    explicit Server(int port);
    ~Server();

    void start(volatile bool& running);
};

#endif
