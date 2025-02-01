#ifndef WEBSOCKET_H
#define WEBSOCKET_H

#include <string>

class WebSocket {
public:
    // Receives a single WebSocket frame, returning its payload as a string.
    // connectionOpen: set to false if the client disconnects or an error occurs.
    // opcodeOut: the opcode of the received frame (e.g., 0x1 for text, 0x2 for binary, etc.).
    static std::string receiveFrame(int clientSocket, bool &connectionOpen, unsigned char &opcodeOut);

    // Sends a single WebSocket frame to the client.
    // opcode defaults to 0x1 (text). Use 0x2 for binary, 0x8 for close, etc.
    static void sendFrame(int clientSocket, const std::string &message, unsigned char opcode = 0x1);
};

#endif // WEBSOCKET_H
