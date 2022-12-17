#pragma once
#include <unordered_map>
#include <utility>
#include <Windows.h>

#include "BlenderObj.h"

enum class PatchVersion
{
    PatchToPrintF,

    PatchToDropEvent,
};


struct BlenderPatch
{
private:
    PatchVersion _version;

    // reference of wm_window.c#ghost_event_proc -> sloc:printf("drop file %s\n");
    std::string _wm_window_ghost_event_proc_printf;

    // reference of func:bpy_interface.c#BPY_run_string_eval
    std::string _bpy_interface_BPY_run_string_eval;

    // reference of func:space_view3d.c#view3d_ima_empty_drop_poll
    std::string _space_view3d_view3d_ima_empty_drop_poll;

    // reference of func:space_view3d.c#view3d_ima_drop_poll
    std::string _space_view3d_view3d_ima_drop_poll;

    // reference of func:view3d_select.c#ED_view3d_give_object_under_cursor
    std::string _view3d_select_ED_view3d_give_object_under_cursor;

    // dictionary of byte-pattern and memory pointer
    std::unordered_map<std::string, std::uintptr_t> _dict = {};
    std::unordered_map<std::string, std::intptr_t> _offsets = {};

    [[nodiscard]] std::uintptr_t GetInjectionLocationFor(std::string instruction) const;

    [[nodiscard]] std::intptr_t GetRelativeOffsetFor(std::string instruction) const;

    [[nodiscard]] std::uintptr_t GetFunctionPointerFor(std::string instruction);

    template <class... TArgs>
    void StoreMemoryPointers(TArgs... args);

    template <class TReturn, class... TArgs>
    TReturn InvokeFunction(std::string instruction, TArgs... args) const;

public:
    BlenderPatch(
        std::string wm_window_ghost_event_proc_printf
    ) : _wm_window_ghost_event_proc_printf(std::move(wm_window_ghost_event_proc_printf))
    {
        _version = PatchVersion::PatchToPrintF;
        StoreMemoryPointers(_wm_window_ghost_event_proc_printf);
    }

    BlenderPatch(
        std::string bpy_interface_BPY_run_string_eval,
        std::string space_view3d_view3d_ima_empty_drop_poll,
        std::string space_view3d_view3d_ima_drop_poll,
        std::string view3d_select_ED_view3d_give_object_under_cursor
    )
        : _bpy_interface_BPY_run_string_eval(std::move(bpy_interface_BPY_run_string_eval)),
          _space_view3d_view3d_ima_empty_drop_poll(std::move(space_view3d_view3d_ima_empty_drop_poll)),
          _space_view3d_view3d_ima_drop_poll(std::move(space_view3d_view3d_ima_drop_poll)),
          _view3d_select_ED_view3d_give_object_under_cursor(std::move(view3d_select_ED_view3d_give_object_under_cursor))
    {
        _version = PatchVersion::PatchToDropEvent;
        StoreMemoryPointers(_bpy_interface_BPY_run_string_eval, _space_view3d_view3d_ima_empty_drop_poll, _space_view3d_view3d_ima_drop_poll, _view3d_select_ED_view3d_give_object_under_cursor);
    }

    [[nodiscard]] PatchVersion GetPatchVersion() const;

    [[nodiscard]] std::uintptr_t Get_view3d_ima_empty_drop_poll() const;

    void BPY_run_string_eval(void* c, const char* imports[], const char* expression) const;

    bool view3d_ima_drop_poll(Context* c, wmDrag* drag, wmEvent* event) const;

    void* ED_view3d_give_object_under_cursor(Context*, int [2]) const;
};


// PATCH LOCATION (search: "drop file" as ANSI string)
//
// XXX: LEA RCX, QWORD PTR [00007FF6754721A0H]     // RCX      = ptr:drop file %s\n
// XXX: MOV RDX, QWORD PTR [RDX]                   // RDX      = ptr:RDX
// XXX: CALL 00007FF66E3E1710H <- here             // printf(RCX, RDX);
//
//
// FUNCTION LOCATION - BPY_run_string_eval (search: "addon_utils.disable_all()" as ANSI string)
//
// XXX: LEA RAX, QWORD PTR [00007FF625E46700H]     // RAX      = ptr:addon_utils
// XXX: MOV QWORD PTR [RSP+38H], 0000000000000000H // [RSP+38] = NULL
// XXX: LEA R8, QWORD PTR [00007FF625E46740H]      // R8       = ptr:addon_utils.disable_all()
// XXX: MOV QWORD PTR [RSP+30H], RAX               // [RSP+30] = ptr:RAX
// XXX: LEA RDX, QWORD PTR [RSP+30H]               // RDX      = ptr:[addon_utils, NULL]
// XXX: MOV RCX, RSI                               // RCX      = ptr:C
// XXX: CALL 00007FF61FF9E3A0H <- here             // BPY_run_string_eval(RCX, RDX, R8)
//
//
// FUNCTION LOCATION - view3d_ima_empty_drop_poll / view3d_id_path_drop_copy (search: "OBJECT_OT_drop_named_image" as ANSI string)
//
// XXX: LEA R9, QWORD PTR [00007FF7F2CAA530H]      // R9       = ptr:view3d_id_path_drop_copy
// XXX: MOV QWORD PTR [RSP+28H], R14               // [RSP+28] = /* unknown */
// XXX: LEA R8, QWORD PTR [00007FF7F2CAA7C0H]      // R8       = ptr:view3d_ima_empty_drop_poll
// XXX: MOV QWORD PTR [RSP+20H], R15               // [RSP+20] = /* unknown */
// XXX: LEA RDX, QWORD PTR [00007FF7F85F02A8H]     // RDX      = ptr:OBJECT_OT_drop_named_image
// XXX: MOV RCX, RBX                               // RBX      = ListBase
// XXX: CALL 00007FF7F2102380H
static std::unordered_map<std::string, BlenderPatch> Patchers{
    // MEM ADDRESS  : '02BC8CC5 - '02BC8CCF
    // MEM PATTERN  : E8 5C 7B C5 FF
    // MEM ASSEMBLY : CALL 00007FF602820830H
    // ref: https://github.com/blender/blender/blob/v3.1.0/source/blender/windowmanager/intern/wm_window.c#L1393
    {"3.1.0", {"E8 5C 7B C5 FF"}},

    // MEM ADDRESS  : 'C6CD8FA5 - 'C6CD8FAF
    // MEM PATTERN  : E8 7C 78 C5 FF
    // MEM ASSEMBLY : CALL 00007FF7C6930830H
    // ref: https://github.com/blender/blender/blob/v3.1.1/source/blender/windowmanager/intern/wm_window.c#L1393
    {"3.1.1", {"E8 7C 78 C5 FF"}},

    // MEM ADDRESS  : '7BD18FA5 - '7BD18FAF
    // MEM PATTERN  : E8 7C 78 C5 FF
    // MEM ASSEMBLY : CALL 00007FF67B970830
    // ref: https://github.com/blender/blender/blob/v3.1.2/source/blender/windowmanager/intern/wm_window.c#L1390
    {"3.1.2", {"E8 7C 78 C5 FF"}},

    // MEM ADDRESS  : 'D3AB57AD - 'D3AB57B7
    // MEM PATTERN  : E8 84 BE 0D FF
    // MEM ASSEMBLY : CALL 00007FF6D2B91640H
    // ref: https://github.com/blender/blender/blob/v3.2.0/source/blender/windowmanager/intern/wm_window.c#L1381
    {"3.2.0", {"E8 84 BE 0D FF"}},

    // MEM ADDRESS  : '32FA5890 - '32FA589A
    // MEM PATTERN  : E8 A1 BD 0D FF
    // MEM ASSEMBLY : CALL 00007FF732081640H
    // ref: https://github.com/blender/blender/blob/v3.2.1/source/blender/windowmanager/intern/wm_window.c#L1383
    {"3.2.1", {"E8 A1 BD 0D FF"}},

    // MEM ADDRESS  : 'A88E58F0 - 'A88E58FA
    // MEM PATTERN  : E8 41 BD 0D FF
    // MEM ASSEMBLY : CALL 00007FF6A79C1640H
    // ref: https://github.com/blender/blender/blob/v3.2.2/source/blender/windowmanager/intern/wm_window.c#L1383
    {"3.2.2", {"E8 41 BD 0D FF"}},

    // MEM ADDRESS  : '8FF9532E - '8FF95338
    // MEM PATTERN  : E8 D3 C3 0E FF
    // MEM ASSEMBLY : CALL 00007FF78F081710H
    // ref: https://github.com/blender/blender/blob/v3.3.0/source/blender/windowmanager/intern/wm_window.c#L1396
    {"3.3.0", {"E8 D3 C3 0E FF"}},

    // MEM ADDRESS  : '6F2F543E - '6F2F5448
    // MEM PATTERN  : E8 C3 C2 0E FF
    // MEM ASSEMBLY : CALL 00007FF66E3E1710H
    // ref: https://github.com/blender/blender/blob/v3.3.1/source/blender/windowmanager/intern/wm_window.c#L1396
    {"3.3.1", {"E8 C3 C2 0E FF"}},

    // MEM ADDRESS  : '1FC0649E - '1FC064A8
    // MEM PATTERN  : E8 23 C3 0E FF
    // MEM ASSEMBLY : CALL 00007FF61ECF27D0H
    // ref: https://github.com/blender/blender/blob/v3.3.2/source/blender/windowmanager/intern/wm_window.c#L1396
    {
        "3.3.2",
        {
            "E8 6E BF 39 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 CB 2C 00 00 48 85 C0"
        }
    },
};
