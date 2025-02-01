#include "HttpRequest.h"
#include <unistd.h>
#include <sstream>
#include <cstring>
#include <algorithm>

HttpRequest::HttpRequest(int clientSocket) {
    char buffer[2048];
    memset(buffer, 0, sizeof(buffer));
    read(clientSocket, buffer, sizeof(buffer) - 1);

    std::istringstream requestStream(buffer);
    requestStream >> method >> path;

    // Parse headers from the request
    parseHeaders(buffer);
}

void HttpRequest::parseHeaders(const std::string& request) {
    std::istringstream stream(request);
    std::string line;

    // Skip the request line (e.g., "GET /path HTTP/1.1")
    std::getline(stream, line);

    // Parse headers
    while (std::getline(stream, line) && line != "\r") {
        size_t delimiterPos = line.find(":");
        if (delimiterPos != std::string::npos) {
            std::string key = line.substr(0, delimiterPos);
            std::string value = line.substr(delimiterPos + 1);

            // Trim spaces
            key.erase(key.find_last_not_of(" \r\n") + 1);
            value.erase(0, value.find_first_not_of(" \r\n"));

            headers[key] = value;
        }
    }
}

std::string HttpRequest::getMethod() const {
    return method;
}

std::string HttpRequest::getPath() const {
    return path;
}

std::string HttpRequest::getHeader(const std::string& headerName) const {
    auto it = headers.find(headerName);
    if (it != headers.end()) {
        return it->second;
    }
    return "";
}