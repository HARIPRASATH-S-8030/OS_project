cmake_minimum_required(VERSION 3.15)
project(SecureFileDestructor VERSION 1.0)

# Enforce C++20 standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Enable strict warnings for code quality
add_compile_options(-Wall -Wextra -Werror)

# Include backend source
add_executable(loader src/backend/loader.cpp)

# Link cryptographic libraries (OpenSSL example)
# Make sure to install OpenSSL on all team machines
find_package(OpenSSL REQUIRED)
target_link_libraries(loader PRIVATE OpenSSL::Crypto OpenSSL::SSL)

# Lock memory primitives (Link with system libraries if needed)
if(WIN32)
    target_link_libraries(loader PRIVATE kernel32)
endif()
