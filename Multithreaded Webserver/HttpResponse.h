#ifndef HTTPRESPONSE_H
#define HTTPRESPONSE_H

#include <string>

class HttpResponse {
private:
    int clientSocket;

public:
    explicit HttpResponse(int clientSocket);

    void send(int statusCode, const std::string& statusMessage, const std::string& body);
    void sendError(int statusCode, const std::string& statusMessage);
};

#endif