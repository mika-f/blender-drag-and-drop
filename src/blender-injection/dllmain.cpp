// dllmain.cpp : Defines the entry point for the DLL application.

// ReSharper disable CppClangTidyClangDiagnosticFormatNonliteral

#include "pch.h"

#include "BlenderPatcher.h"

HANDLE hThread;


DWORD WINAPI BackgroundMonitor(LPVOID pData)
{
    LaunchDebugger();
    BlenderPatcher::GetInstance()->Patch();

    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call) // NOLINT(hicpp-multiway-paths-covered)
    {
    case DLL_PROCESS_ATTACH:
        hThread = CreateThread(nullptr, 0, BackgroundMonitor, nullptr, 0, nullptr);
        if (hThread == nullptr)
            std::cout << "failed to create background thread" << std::endl;

        break;

    case DLL_PROCESS_DETACH:
        CloseHandle(hThread);
        break;

    default:
        break;
    }

    return TRUE;
}
