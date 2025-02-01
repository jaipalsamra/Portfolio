#ifndef HTTPREQUEST_H
#define HTTPREQUEST_H

#include <string>
#include <map>

class HttpRequest {
private:
    std::string method;
    std::string path;
    std::map<std::string, std::string> headers;  // To store HTTP headers

    void parseHeaders(const std::string& request);  // Helper to parse headers

public:
    explicit HttpRequest(int clientSocket);

    std::string getMethod() const;
    std::string getPath() const;
    std::string getHeader(const std::string& headerName) const;  // New method
};

#endif
