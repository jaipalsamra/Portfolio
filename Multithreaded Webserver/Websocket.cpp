#include "Websocket.h"
#include <unistd.h>      // for close(), read(), etc.
#include <vector>
#include <iostream>
#include <cstring>
#include <sys/socket.h>  // for send(), recv()

std::string WebSocket::receiveFrame(int clientSocket, bool &connectionOpen, unsigned char &opcodeOut) {
    unsigned char header[2];
    int bytesRead = recv(clientSocket, header, 2, 0);
    if (bytesRead <= 0) {
        connectionOpen = false;
        return "";
    }

    bool fin = (header[0] & 0x80) != 0;       // FIN bit
    unsigned char opcode = header[0] & 0x0F; // lower 4 bits => opcode
    bool masked = (header[1] & 0x80) != 0;    // Mask bit
    uint64_t payloadLength = header[1] & 0x7F;

    // Extended payload length
    if (payloadLength == 126) {
        unsigned char ext[2];
        recv(clientSocket, ext, 2, 0);
        payloadLength = (ext[0] << 8) | ext[1];
    } else if (payloadLength == 127) {
        unsigned char ext[8];
        recv(clientSocket, ext, 8, 0);
        payloadLength = 0;
        for (int i = 0; i < 8; ++i) {
            payloadLength = (payloadLength << 8) | ext[i];
        }
    }

    // Read the masking key if masked
    unsigned char maskKey[4] = {0};
    if (masked) {
        recv(clientSocket, maskKey, 4, 0);
    }

    // Read the payload
    std::vector<unsigned char> payload(payloadLength);
    size_t totalReceived = 0;
    while (totalReceived < payloadLength) {
        int chunk = recv(clientSocket, payload.data() + totalReceived, payloadLength - totalReceived, 0);
        if (chunk <= 0) {
            connectionOpen = false;
            return "";
        }
        totalReceived += chunk;
    }

    // Unmask client-to-server frames if needed
    if (masked) {
        for (size_t i = 0; i < payloadLength; ++i) {
            payload[i] ^= maskKey[i % 4];
        }
    }

    opcodeOut = opcode;
    return std::string(payload.begin(), payload.end());
}

void WebSocket::sendFrame(int clientSocket, const std::string &message, unsigned char opcode) {
    unsigned char header[10];
    size_t headerSize = 2;
    size_t messageLength = message.size();

    // FIN bit + opcode
    header[0] = 0x80 | opcode;

    // Determine payload length
    if (messageLength <= 125) {
        header[1] = messageLength;
    } else if (messageLength <= 65535) {
        header[1] = 126;
        header[2] = (messageLength >> 8) & 0xFF;
        header[3] = messageLength & 0xFF;
        headerSize += 2;
    } else {
        header[1] = 127;
        for (int i = 0; i < 8; i++) {
            header[2 + i] = (messageLength >> (56 - 8 * i)) & 0xFF;
        }
        headerSize += 8;
    }

    send(clientSocket, header, headerSize, 0);
    send(clientSocket, message.data(), messageLength, 0);
}
