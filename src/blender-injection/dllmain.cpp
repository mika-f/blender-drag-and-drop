// dllmain.cpp : Defines the entry point for the DLL application.
#include "pch.h"

#include <ImageHlp.h>
#include <Windows.h>

#pragma comment(lib, "imagehlp.lib")

HANDLE hThread;

#ifdef BLENDER_3_1_0
// MEM ADDRESS  : '02BC8CC5 - '02BC8CCF
// MEM PATTERN  : E8 5C 7B C5 FF
// MEM ASSEMBLY : CALL 00007FF602820830H
// ref: https://github.com/blender/blender/blob/v3.1.0/source/blender/windowmanager/intern/wm_window.c#L1393
#define BYTE_PATTERN "E8 5C 7B C5 FF"
#define BYTE_OFFSET  17
#elif defined(BLENDER_3_1_1)
// MEM ADDRESS  : 'C6CD8FA5 - 'C6CD8FAF
// MEM PATTERN  : E8 7C 78 C5 FF
// MEM ASSEMBLY : CALL 00007FF7C6930830H
// ref: https://github.com/blender/blender/blob/v3.1.1/source/blender/windowmanager/intern/wm_window.c#L1393
#define BYTE_PATTERN "E8 7C 78 C5 FF"
#define BYTE_OFFSET  17
#elif defined(BLENDER_3_1_2)
// MEM ADDRESS  : '7BD18FA5 - '7BD18FAF
// MEM PATTERN  : E8 7C 78 C5 FF
// MEM ASSEMBLY : CALL 00007FF67B970830
// ref: https://github.com/blender/blender/blob/v3.1.2/source/blender/windowmanager/intern/wm_window.c#L1390
#define BYTE_PATTERN "E8 7C 78 C5 FF"
#define BYTE_OFFSET  17
#elif defined(BLENDER_3_2_0)
// MEM ADDRESS  : 'D3AB57AD - 'D3AB57B7
// MEM PATTERN  : E8 84 BE 0D FF
// MEM ASSEMBLY : CALL 00007FF6D2B91640H
// ref: https://github.com/blender/blender/blob/v3.2.0/source/blender/windowmanager/intern/wm_window.c#L1381
#define BYTE_PATTERN "E8 84 BE 0D FF"
#define BYTE_OFFSET  17
#elif defined(BLENDER_3_2_1)
// MEM ADDRESS  : '32FA5890 - '32FA589A
// MEM PATTERN  : E8 A1 BD 0D FF
// MEM ASSEMBLY : CALL 00007FF732081640H
// ref: https://github.com/blender/blender/blob/v3.2.1/source/blender/windowmanager/intern/wm_window.c#L1383
#define BYTE_PATTERN "E8 A1 BD 0D FF"
#define BYTE_OFFSET  17
#elif defined(BLENDER_3_2_2)
// MEM ADDRESS  : 'A88E58F0 - 'A88E58FA
// MEM PATTERN  : E8 41 BD 0D FF
// MEM ASSEMBLY : CALL 00007FF6A79C1640H
// ref: https://github.com/blender/blender/blob/v3.2.2/source/blender/windowmanager/intern/wm_window.c#L1383
#define BYTE_PATTERN "E8 41 BD 0D FF"
#define BYTE_OFFSET  17
#elif defined(BLENDER_3_3_0)
// MEM ADDRESS  : '8FF9532E - '8FF95338
// MEM PATTERN  : E8 D3 C3 0E FF
// MEM ASSEMBLY : CALL 00007FF78F081710H
// ref: https://github.com/blender/blender/blob/v3.3.0/source/blender/windowmanager/intern/wm_window.c#L1396
#define BYTE_PATTERN "E8 D3 C3 0E FF"
#define BYTE_OFFSET  17
#else
#define BYTE_PATTERN ""
#define BYTE_OFFSET  0
#endif


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
    BytePattern::temp_instance().find_pattern(BYTE_PATTERN);
    if (BytePattern::temp_instance().count() > 0)
    {
        SetConsoleOutputCP(CP_UTF8);
        setvbuf(stdout, nullptr, _IOFBF, 1000);

        const auto address = BytePattern::temp_instance().get_first().address();
        Injector::MakeInline<RedirectToAttachedConsole>(address, address + BYTE_OFFSET);
    }
    else
    {
        std::cout << "failed to find byte pattern such as `" << BYTE_PATTERN << "`" << std::endl;
        std::cout << "Are you using matched version of Blender?" << std::endl;
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
