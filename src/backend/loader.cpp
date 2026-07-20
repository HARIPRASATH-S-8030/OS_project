#include <iostream>

#ifdef _WIN32
    #include <windows.h>
#endif

bool LockSensitiveData(void* ptr, size_t size) {
#ifdef _WIN32
    if (VirtualLock(ptr, size)) {
        return true;
    }
    std::cerr << "Failed to lock memory. Error: " << GetLastError() << std::endl;
    return false;
#else
    (void)ptr; // Explicitly mark as unused
    (void)size; // Explicitly mark as unused
    std::cout << "VirtualLock not supported on this platform." << std::endl;
    return false;
#endif
}

void DecryptPayload(void* encryptedData, size_t size) {
    (void)encryptedData; // Explicitly mark as unused
    (void)size;          // Explicitly mark as unused
    std::cout << "DecryptPayload shell called." << std::endl;
}

int main() {
    size_t size = 1024;
#ifdef _WIN32
    void* buffer = VirtualAlloc(NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);
    if (buffer == NULL) return 1;

    if (LockSensitiveData(buffer, size)) {
        std::cout << "Memory successfully locked and pinned in RAM." << std::endl;
    }
    DecryptPayload(buffer, size);
    VirtualFree(buffer, 0, MEM_RELEASE);
#else
    std::cout << "Running on non-Windows environment. Memory locking skipped." << std::endl;
    DecryptPayload(nullptr, size);
#endif
    return 0;
}
