// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"

#include <cstdio>
#include <iostream>
#include <string>
#include <Windows.h>


HANDLE hThread;

DWORD WINAPI BackgroundMonitor(LPVOID pData)
{
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call) // NOLINT(hicpp-multiway-paths-covered)
    {
    case DLL_PROCESS_ATTACH:
        hThread = CreateThread(nullptr, 0, &BackgroundMonitor, nullptr, 0, nullptr);
        if (hThread == nullptr)
            printf("failed to create background thread");

        break;

    case DLL_PROCESS_DETACH:
        CloseHandle(hThread);
    default: ;
    }

    return TRUE;
}
