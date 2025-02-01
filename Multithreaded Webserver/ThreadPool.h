#ifndef THREADPOOL_H
#define THREADPOOL_H

#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <condition_variable>
#include <functional>
#include <atomic>

class ThreadPool {
private:
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex mtx;
    std::condition_variable cv;
    std::atomic<bool> stop;

    void worker();

public:
    explicit ThreadPool(size_t numThreads);
    ~ThreadPool();

    void enqueue(std::function<void()> task);
};
#endif