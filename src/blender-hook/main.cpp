// blender-hook.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <clocale>
#include <cstdio>
#include <iostream>
#include <Windows.h>

int main(int argc, char* argv[])
{
    char path[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, path);
    strcat_s(path, sizeof(path), "\\blender-injection.dll");

    const auto pid = strtoul(argv[1], nullptr, 0);
    const auto hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    if (!hProcess)
    {
        std::cout << "failed to open process" << std::endl;
        return EXIT_FAILURE;
    }

    const auto lpBaseAddress = VirtualAllocEx(hProcess, nullptr, sizeof(path) + 1, MEM_COMMIT, PAGE_READWRITE);
    if (!lpBaseAddress)
    {
        std::cout << "failed to load VirtualAllocEx" << std::endl;
        return EXIT_FAILURE;
    }

    WriteProcessMemory(hProcess, lpBaseAddress, path, sizeof(path) + 1, nullptr);

    const auto kernel32 = LoadLibraryW(L"kernel32");
    if (!kernel32)
    {
        std::cout << "failed to load kernel32.dll" << std::endl;
        return EXIT_FAILURE;
    }
    const auto address = GetProcAddress(kernel32, "LoadLibraryA");
    const auto hThread = CreateRemoteThread(hProcess, nullptr, 0, (LPTHREAD_START_ROUTINE)address, lpBaseAddress, 0, nullptr);

    if (!hThread)
    {
        wchar_t msg[512];
        FormatMessageW(FORMAT_MESSAGE_FROM_SYSTEM, nullptr, GetLastError(), 0, msg, sizeof(msg), nullptr);
        std::cout << msg << std::endl;

        return EXIT_FAILURE;
    }

    const auto hResult = WaitForSingleObject(hThread, INFINITE);
    if (!hResult)
    {
        wchar_t msg[512];
        FormatMessageW(FORMAT_MESSAGE_FROM_SYSTEM, nullptr, GetLastError(), 0, msg, sizeof(msg), nullptr);
        std::cout << msg << std::endl;

        return EXIT_FAILURE;
    }

    CloseHandle(hThread);

    return EXIT_SUCCESS;
}
