#include <iostream>
#include <vector>
#include <string>

#ifdef _WIN32
#include <windows.h>
#else
#include <sys/mman.h>
#include <cstring>
#endif

// Secure memory sanitization function
void secure_sanitize(volatile char* ptr, size_t size) {
    #ifdef _WIN32
    SecureZeroMemory((void*)ptr, size);
    #else
    // Explicitly zero out memory to prevent compiler optimization removal
    typedef void* (*memset_t)(void*, int, size_t);
    volatile memset_t secure_memset = memset;
    secure_memset((void*)ptr, 0, size);
    #endif
}

int main() {
    std::cout << "[Backend C++] Initialized and waiting for payload..." << std::endl;

    const size_t data_size = 1024 * 1024; // 1 MB sensitive buffer example
    std::vector<char> secure_buffer(data_size, 'A'); // Simulated sensitive data

    // OS-level Memory Pinning (VirtualLock / mlock)
    #ifdef _WIN32
    if (!VirtualLock(secure_buffer.data(), data_size)) {
        std::cerr << "[Backend C++] VirtualLock failed!" << std::endl;
    } else {
        std::cout << "[Backend C++] Memory successfully pinned via VirtualLock." << std::endl;
    }
    #else
    if (mlock(secure_buffer.data(), data_size) != 0) {
        std::cerr << "[Backend C++] mlock failed!" << std::endl;
    } else {
        std::cout << "[Backend C++] Memory successfully pinned via mlock." << std::endl;
    }
    #endif

    // Listen for signal from Python Policy Engine via stdin
    std::string command;
    while (std::cin >> command) {
        if (command == "SANITIZE" || command == "EXIT") {
            std::cout << "[Backend C++] Sanitization signal received from Policy Engine." << std::endl;
            
            // Execute Zero-Residual Sanitization
            secure_sanitize(secure_buffer.data(), data_size);
            std::cout << "[Backend C++] Memory buffer overwritten with zero-residuals." << std::endl;

            // Release lock
            #ifdef _WIN32
            VirtualUnlock(secure_buffer.data(), data_size);
            #else
            munlock(secure_buffer.data(), data_size);
            #endif

            std::cout << "[Backend C++] Process exiting cleanly." << std::endl;
            break;
        }
    }

    return 0;
}