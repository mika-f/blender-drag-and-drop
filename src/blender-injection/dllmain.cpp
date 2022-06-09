// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"

#include <ImageHlp.h>
#include <Windows.h>

#pragma comment(lib, "imagehlp.lib")

HANDLE hThread;

struct RedirectToAttachedConsole
{
    void operator()(Injector::reg_pack& regs) const
    {
        const auto addr = regs.rdx;
        const auto str = (char*)addr.i;

        // if this line is too long, DLL throw access violation exception
        std::cout << "f:" << str << std::endl;
    }
};

DWORD WINAPI BackgroundMonitor(LPVOID pData)
{
    // MEM ADDR: XXXX'7BD18FA5 - XXXX'7BD18FAF
    // MEM PTRN: E8 7C 78 C5 FF
    // MEM ASM : CALL 00007FF67B970830
    // ref: https://github.com/blender/blender/blob/594f47ecd2d5367ca936cf6fc6ec8168c2b360d0/source/blender/windowmanager/intern/wm_window.c#L1462
    BytePattern::temp_instance().find_pattern("E8 7C 78 C5 FF");
    if (BytePattern::temp_instance().count() > 0)
    {
        const auto address = BytePattern::temp_instance().get_first().address();
        // Injector::MakeRangedNOP(address, address + 17);
        // Injector::MakeCALL(address, address + 17, false);
        Injector::MakeInline<RedirectToAttachedConsole>(address, address + 17);
    }
    else
    {
        std::cout << "failed to find byte pattern such as `E8 7C 78 C5 FF` (ASM: CALL 00007FF67B970830)" << std::endl;
        std::cout << "Are you using Blender 3.1.2?" << std::endl;
    }
    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
    switch (ul_reason_for_call) // NOLINT(hicpp-multiway-paths-covered)
    {
    case DLL_PROCESS_ATTACH:
        hThread = CreateThread(nullptr, 0, &BackgroundMonitor, nullptr, 0, nullptr);
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
