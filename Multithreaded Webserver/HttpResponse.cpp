#include "HttpResponse.h"
#include <unistd.h>
#include <sstream>
#include <sys/socket.h> // Include for `send`

HttpResponse::HttpResponse(int clientSocket) : clientSocket(clientSocket) {}

void HttpResponse::send(int statusCode, const std::string& statusMessage, const std::string& body) {
    std::ostringstream response;
    response << "HTTP/1.1 " << statusCode << " " << statusMessage << "\r\n";
    response << "Content-Length: " << std::to_string(body.size()) << "\r\n\r\n"; // Convert size to string
    response << body;
    std::string responseStr = response.str();
    ::send(clientSocket, responseStr.c_str(), responseStr.size(), 0); // Use the global send function
}

void HttpResponse::sendError(int statusCode, const std::string& statusMessage) {
    std::ostringstream response;
    response << "HTTP/1.1 " << statusCode << " " << statusMessage << "\r\n\r\n";
    std::string responseStr = response.str();
    ::send(clientSocket, responseStr.c_str(), responseStr.size(), 0);
}
