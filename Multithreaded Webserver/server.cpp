#include "server.h"
#include "Websocket.h"
#include <sstream>
#include <iostream>
#include <unistd.h>
#include <cstring>
#include <fstream>

// Existing Server::handleClient, Server::handleWebSocketHandshake, etc.

void Server::handleWebSocket(int clientSocket) {
    bool connectionOpen = true;

    while (connectionOpen) {
        unsigned char opcode;
        std::string payload = WebSocket::receiveFrame(clientSocket, connectionOpen, opcode);

        if (!connectionOpen) {
            break; // socket closed or error
        }

        switch (opcode) {
            case 0x1:  // Text
                std::cout << "Received Text: " << payload << std::endl;
                // Echo back
                WebSocket::sendFrame(clientSocket, "Echo: " + payload, 0x1);
                break;
            case 0x2:  // Binary
                // ...
                break;
            case 0x8:  // Close
                WebSocket::sendFrame(clientSocket, "", 0x8);
                connectionOpen = false;
                break;
            case 0x9:  // Ping
                // Respond with Pong
                WebSocket::sendFrame(clientSocket, payload, 0xA);
                break;
            case 0xA:  // Pong
                std::cout << "Received Pong" << std::endl;
                break;
            default:
                std::cout << "Unknown opcode: " << std::hex << (int)opcode << std::endl;
                break;
        }
    }

    close(clientSocket);
}
