#pragma once
#include <unordered_map>
#include <utility>
#include <Windows.h>

struct BlenderPatch
{
private:
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

    [[nodiscard]] static std::uintptr_t GetInjectionLocationFor(std::string instruction);

    [[nodiscard]] std::intptr_t GetRelativeOffsetFor(std::string instruction) const;

    [[nodiscard]] std::uintptr_t GetFunctionPointerFor(std::string instruction) const;

    template <class... TArgs>
    void StoreMemoryPointers(TArgs... args);

    template <class TReturn, class... TArgs>
    TReturn InvokeFunction(std::string instruction, TArgs... args) const;

public:
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
        StoreMemoryPointers(
            _bpy_interface_BPY_run_string_eval,
            _space_view3d_view3d_ima_empty_drop_poll,
            _space_view3d_view3d_ima_drop_poll,
            _view3d_select_ED_view3d_give_object_under_cursor
        );
    }

    [[nodiscard]] std::uintptr_t Get_view3d_ima_empty_drop_poll() const;

    void BPY_run_string_eval(void* c, const char* imports[], const char* expression) const;

    bool view3d_ima_drop_poll(void* c, void* drag, void* event) const;

    void* ED_view3d_give_object_under_cursor(void*, int [2]) const;
};

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
//
//
// FUNCTION LOCATION - view3d_ima_drop_poll (visit: "view3d_ima_empty_drop_poll" and first CALL)
//
// FUNCTION LOCATION - ED_view3d_give_object_under_cursor (visit: "view3d_ima_empty_drop_poll" and second CALL)
static std::unordered_map<std::string, BlenderPatch> Patchers{
    {
        "3.3.2",
        {
            "E8 6E BF 39 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 CB 2C 00 00 48 85 C0"
        },
    },
    {
        "3.4.0",
        {
            "E8 2E 7A 3C 00",
            "4C 8D 05 B7 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 FB B6 00 00 48 85 C0"
        }
    },
    {
        "3.4.1",
        {
            "E8 48 C0 3C 00",
            "4C 8D 05 B7 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 FB B6 00 00 48 85 C0"
        }
    }
};
