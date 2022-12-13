// dllmain.cpp : Defines the entry point for the DLL application.

// ReSharper disable CppClangTidyClangDiagnosticFormatNonliteral

#include "pch.h"

#include <string>
#include <unordered_map>
#include <Windows.h>

#pragma comment(lib, "version.lib")

HANDLE hThread;
unsigned long long hRunEvaluator;

extern "C" void InvokeForceStdOut(const char*, char*);
extern "C" void InvokePythonInterpreter(unsigned long long, void*, const char*[], const char*);

struct Context
{
    int thread;

    struct
    {
        void* manager;
        void* window;
        void* workspace;
        void* screen;
        void* area;
        void* region;
        void* menu;
        void* gizmo_group;
        void* store;

        const char* operator_poll_msg;

        struct PollMsgDyn_Params
        {
            char* (*get_fn)(Context*, void*);
            char* (*free_fn)(Context*, void*);
            void* user_data;
        } operator_poll_msg_dyn_params;
    } wm;

    struct
    {
        void* main;
        void* scene;
        int recursion;
        bool py_init;
        void* py_context;
        void* py_context_orig;
    } data;
};

struct Patch
{
    // old approach
    std::string BytePattern;
    short Offset;

    // new approach
    unsigned long long FunctionPointer;
};


// PATCH LOCATION (search: "drop file" as ANSI string)
//
// XXX: LEA RCX, QWORD PTR [00007FF6754721A0H]     // RCX      = ptr:drop file %s\n
// XXX: MOV RDX, QWORD PTR [RDX]                   // RDX      = ptr:RDX
// XXX: CALL 00007FF66E3E1710H <- here             // printf(RCX, RDX);
//
//
// FUNCTION LOCATION (search: "addon_utils.disable_all()" as ANSI string)
//
// XXX: LEA RAX, QWORD PTR [00007FF625E46700H]     // RAX      = ptr:addon_utils
// XXX: MOV QWORD PTR [RSP+38H], 0000000000000000H // [RSP+38] = NULL
// XXX: LEA R8, QWORD PTR [00007FF625E46740H]      // R8       = ptr:addon_utils.disable_all()
// XXX: MOV QWORD PTR [RSP+30H], RAX               // [RSP+30] = ptr:RAX
// XXX: LEA RDX, QWORD PTR [RSP+30H]               // RDX      = ptr:[addon_utils, NULL]
// XXX: MOV RCX, RSI                               // RCX      = ptr:C
// XXX: CALL 00007FF61FF9E3A0H <- here             // BPY_run_string_eval(RCX, RDX, R8)
// 
std::unordered_map<std::string, Patch> patchers{
    // MEM ADDRESS  : '02BC8CC5 - '02BC8CCF
    // MEM PATTERN  : E8 5C 7B C5 FF
    // MEM ASSEMBLY : CALL 00007FF602820830H
    // ref: https://github.com/blender/blender/blob/v3.1.0/source/blender/windowmanager/intern/wm_window.c#L1393
    {"3.1.0", {"E8 5C 7B C5 FF", 17, 0}},

    // MEM ADDRESS  : 'C6CD8FA5 - 'C6CD8FAF
    // MEM PATTERN  : E8 7C 78 C5 FF
    // MEM ASSEMBLY : CALL 00007FF7C6930830H
    // ref: https://github.com/blender/blender/blob/v3.1.1/source/blender/windowmanager/intern/wm_window.c#L1393
    {"3.1.1", {"E8 7C 78 C5 FF", 17, 0}},

    // MEM ADDRESS  : '7BD18FA5 - '7BD18FAF
    // MEM PATTERN  : E8 7C 78 C5 FF
    // MEM ASSEMBLY : CALL 00007FF67B970830
    // ref: https://github.com/blender/blender/blob/v3.1.2/source/blender/windowmanager/intern/wm_window.c#L1390
    {"3.1.2", {"E8 7C 78 C5 FF", 17, 0}},

    // MEM ADDRESS  : 'D3AB57AD - 'D3AB57B7
    // MEM PATTERN  : E8 84 BE 0D FF
    // MEM ASSEMBLY : CALL 00007FF6D2B91640H
    // ref: https://github.com/blender/blender/blob/v3.2.0/source/blender/windowmanager/intern/wm_window.c#L1381
    {"3.2.0", {"E8 84 BE 0D FF", 17, 0}},

    // MEM ADDRESS  : '32FA5890 - '32FA589A
    // MEM PATTERN  : E8 A1 BD 0D FF
    // MEM ASSEMBLY : CALL 00007FF732081640H
    // ref: https://github.com/blender/blender/blob/v3.2.1/source/blender/windowmanager/intern/wm_window.c#L1383
    {"3.2.1", {"E8 A1 BD 0D FF", 17, 0}},

    // MEM ADDRESS  : 'A88E58F0 - 'A88E58FA
    // MEM PATTERN  : E8 41 BD 0D FF
    // MEM ASSEMBLY : CALL 00007FF6A79C1640H
    // ref: https://github.com/blender/blender/blob/v3.2.2/source/blender/windowmanager/intern/wm_window.c#L1383
    {"3.2.2", {"E8 41 BD 0D FF", 17, 0}},

    // MEM ADDRESS  : '8FF9532E - '8FF95338
    // MEM PATTERN  : E8 D3 C3 0E FF
    // MEM ASSEMBLY : CALL 00007FF78F081710H
    // ref: https://github.com/blender/blender/blob/v3.3.0/source/blender/windowmanager/intern/wm_window.c#L1396
    {"3.3.0", {"E8 D3 C3 0E FF", 17, 0}},

    // MEM ADDRESS  : '6F2F543E - '6F2F5448
    // MEM PATTERN  : E8 C3 C2 0E FF
    // MEM ASSEMBLY : CALL 00007FF66E3E1710H
    // ref: https://github.com/blender/blender/blob/v3.3.1/source/blender/windowmanager/intern/wm_window.c#L1396
    {"3.3.1", {"E8 C3 C2 0E FF", 17, 0}},

    // MEM ADDRESS  : '1FC0649E - '1FC064A8
    // MEM PATTERN  : E8 23 C3 0E FF
    // MEM ASSEMBLY : CALL 00007FF61ECF27D0H
    // ref: https://github.com/blender/blender/blob/v3.3.2/source/blender/windowmanager/intern/wm_window.c#L1396
    {"3.3.2", {"E8 23 C3 0E FF", 17, 0x00007FF7F247E3A0}}
};

template <typename... Args>
std::string format(const std::string& fmt, Args... args)
{
    const auto len = std::snprintf(nullptr, 0, fmt.c_str(), args...);
    std::vector<char> buf(len + 1);
    std::snprintf(buf.data(), len + 1, fmt.c_str(), args...); // NOLINT(cert-err33-c)
    const auto str = std::string(buf.begin(), buf.end());
    return str.substr(0, len); // remove null-terminated string
}

std::string GetVersionFromBinary()
{
    TCHAR filename[MAX_PATH + 1];

    GetModuleFileName(nullptr, filename, sizeof(filename));

    const auto size = GetFileVersionInfoSize(filename, nullptr);

    if (const auto version = new BYTE[size]; GetFileVersionInfo(filename, NULL, size, version))
    {
        unsigned int len;
        VS_FIXEDFILEINFO* pFileInfo;

        VerQueryValue(version, "\\", reinterpret_cast<void**>(&pFileInfo), &len);

        return format("%d.%d.%d", HIWORD(pFileInfo->dwFileVersionMS), LOWORD(pFileInfo->dwFileVersionMS), HIWORD(pFileInfo->dwFileVersionLS));
    }

    return "0.0.0";
}

// Replace CALL assembly with specific destination
void ReplaceWithCall(const Injector::memory_pointer_tr& at, void* dest, unsigned int fill)
{
    // 7FF7'9C5D532E
    unsigned char assembly[] = {
        /* MOV RAX, 0000000000000000h */ 0x48, 0xB8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        /* CALL RAX                   */ 0xFF, 0xD0,
    };

    *reinterpret_cast<void**>(&assembly[2]) = dest;

    Injector::WriteMemoryRaw(at, assembly, sizeof(assembly), true);
}

extern "C" void PrepareForInvokeInterpreter(void* c, char* str)
{
    if (hRunEvaluator > 0)
    {
        const char* imports[] = {"bpy", nullptr};
        const auto expression = "\nbpy.ops.object.drop_event_listener2(\"INVOKE_DEFAULT\", filename=R\"" + std::string(str) + "\")";

        const auto ctx = static_cast<Context*>(c);
        InvokePythonInterpreter(hRunEvaluator, ctx, imports, expression.c_str());
    }
    else
    {
        std::cout << str << std::endl;
    }
}

DWORD WINAPI BackgroundMonitor(LPVOID pData)
{
    try
    {
        const auto version = GetVersionFromBinary();

        const auto [pattern, offset, pointer] = patchers.at(version);

        BytePattern::temp_instance().find_pattern(pattern);
        if (BytePattern::temp_instance().count() > 0)
        {
            SetConsoleOutputCP(CP_UTF8);
            setvbuf(stdout, nullptr, _IOFBF, 1000);

            if (pointer > 0)
                hRunEvaluator = pointer;

            const auto address = BytePattern::temp_instance().get_first().address();
            ReplaceWithCall(address, (void*)(&InvokeForceStdOut), offset);
        }
        else
        {
            std::cout << "failed to find byte pattern such as `" << pattern << "`" << std::endl;
            std::cout << "Are you using matched version of Blender?" << std::endl;
        }
    }
    catch (std::out_of_range&)
    {
        std::cout << "[ERROR] exception: out of range" << std::endl;
        std::cout << "[ERROR] injector detected unsupported version of Blender. Please upgrade this or downgrade Blender." << std::endl;
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
