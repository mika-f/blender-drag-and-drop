#pragma once
#include <unordered_map>

struct BlenderPatchPattern
{
private:
    // <= 3.6.5 reference of func:bpy_interface.c#BPY_run_string_eval
    // >= 4.0.0 reference of func:bpy_interface_run.cc#BPY_run_string_eval
    std::string _bpy_interface_BPY_run_string_eval;

    // <= 3.6.5 reference of func:space_view3d.c#view3d_ima_empty_drop_poll
    // >= 4.0.0 reference of func:space_view3d.cc#view3d_ima_empty_drop_poll
    std::string _space_view3d_view3d_ima_empty_drop_poll;

    // <= 3.6.5 reference of func:space_view3d.c#view3d_ima_drop_poll
    // >= 4.0.0 reference of func:space_view3d.cc#view3d_ima_drop_poll
    std::string _space_view3d_view3d_ima_drop_poll;

    // <= 3.6.5 reference of func:view3d_select.c#ED_view3d_give_object_under_cursor
    // >= 4.0.0 reference of func:view3d_select.cc#ED_view3d_give_object_under_cursor
    std::string _view3d_select_ED_view3d_give_object_under_cursor;

public:
    BlenderPatchPattern(
        std::string bpy_interface_BPY_run_string_eval,
        std::string space_view3d_view3d_ima_empty_drop_poll,
        std::string space_view3d_view3d_ima_drop_poll,
        std::string view3d_select_ED_view3d_give_object_under_cursor)
        : _bpy_interface_BPY_run_string_eval(std::move(bpy_interface_BPY_run_string_eval)),
          _space_view3d_view3d_ima_empty_drop_poll(std::move(space_view3d_view3d_ima_empty_drop_poll)),
          _space_view3d_view3d_ima_drop_poll(std::move(space_view3d_view3d_ima_drop_poll)),
          _view3d_select_ED_view3d_give_object_under_cursor(std::move(view3d_select_ED_view3d_give_object_under_cursor))
    {
    }

    [[nodiscard]] std::string get_bpy_interface_BPY_run_string_eval() const
    {
        return this->_bpy_interface_BPY_run_string_eval;
    }

    [[nodiscard]] std::string get_space_view3d_view3d_ima_empty_drop_poll() const
    {
        return this->_space_view3d_view3d_ima_empty_drop_poll;
    }

    [[nodiscard]] std::string get_space_view3d_view3d_ima_drop_poll() const
    {
        return this->_space_view3d_view3d_ima_drop_poll;
    }

    [[nodiscard]] std::string get_view3d_select_ED_view3d_give_object_under_cursor() const
    {
        return this->_view3d_select_ED_view3d_give_object_under_cursor;
    }
};

// FUNCTION LOCATION       - BPY_run_string_eval (search: "addon_utils.disable_all()" as ANSI string)
// IMPLEMENTATION LOCATION - ANY
//
// XXX: LEA RAX, QWORD PTR [00007FF625E46700H]         // RAX      = ptr:addon_utils
// XXX: MOV QWORD PTR [RSP+38H], 0000000000000000H     // [RSP+38] = NULL
// XXX: LEA R8, QWORD PTR [00007FF625E46740H]          // R8       = ptr:addon_utils.disable_all()
// XXX: MOV QWORD PTR [RSP+30H], RAX                   // [RSP+30] = ptr:RAX
// XXX: LEA RDX, QWORD PTR [RSP+30H]                   // RDX      = ptr:[addon_utils, NULL]
// XXX: MOV RCX, RSI                                   // RCX      = ptr:C
// XXX: CALL 00007FF61FF9E3A0H <- here                 // BPY_run_string_eval(RCX, RDX, R8)
// XXX: CALL 00007FF61FF9E3C0H                         //
//
//
// FUNCTION LOCATION       - view3d_ima_empty_drop_poll / view3d_id_path_drop_copy (search: "OBJECT_OT_drop_named_image" as ANSI string)
// IMPLEMENTATION LOCATION - source/blender/editors/space_view3d/space_view3d.cc
//
// XXX: LEA R9, QWORD PTR [00007FF7F2CAA530H]          // R9       = ptr:view3d_id_path_drop_copy
// XXX: MOV QWORD PTR [RSP+28H], R14                   // [RSP+28] = /* unknown */
// XXX: LEA R8, QWORD PTR [00007FF7F2CAA7C0H] <- here  // R8       = ptr:view3d_ima_empty_drop_poll
// XXX: MOV QWORD PTR [RSP+20H], R15                   // [RSP+20] = /* unknown */
// XXX: LEA RDX, QWORD PTR [00007FF7F85F02A8H]         // RDX      = ptr:OBJECT_OT_drop_named_image
// XXX: MOV RCX, RBX                                   // RBX      = ListBase
// XXX: CALL 00007FF7F2102380H
//
//
// FUNCTION LOCATION - view3d_ima_drop_poll (visit: "view3d_ima_empty_drop_poll" and first CALL)
//
// FUNCTION LOCATION - ED_view3d_give_object_under_cursor (visit: "view3d_ima_empty_drop_poll" and second CALL)

static std::unordered_map<std::string, BlenderPatchPattern> Patchers{
#pragma region Blender 3.x
    {
        "3.1.0",
        {
            "E8 28 BC 3F 00",
            "4C 8D 05 65 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 1B 2D 00 00 48 85 C0",
        },
    },
    {
        "3.1.1",
        {
            "E8 28 C0 3F 00",
            "4C 8D 05 65 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 5B 2C 00 00 48 85 C0",
        },
    },
    {
        "3.1.2",
        {
            "E8 28 C0 3F 00",
            "4C 8D 05 65 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 5B 2C 00 00 48 85 C0",
        },
    },
    {
        "3.2.0",
        {
            "E8 D8 88 3C 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 BB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.2.1",
        {
            "E8 58 91 3C 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 BB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.2.2",
        {
            "E8 78 91 3C 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 BB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.3.0",
        {
            "E8 E8 08 3A 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 CB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.3.1",
        {
            "E8 88 01 3A 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 CB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.3.2",
        {
            "E8 6E BF 39 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 CB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.3.3",
        {
            "E8 3E C0 39 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 CB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.3.4",
        {
            "E8 5E C0 39 00",
            "4C 8D 05 77 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 CB 2C 00 00 48 85 C0",
        },
    },
    {
        "3.4.0",
        {
            "E8 2E 7A 3C 00",
            "4C 8D 05 B7 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 FB B6 00 00 48 85 C0",
        },
    },
    {
        "3.4.1",
        {
            "E8 48 C0 3C 00",
            "4C 8D 05 B7 06 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 FB B6 00 00 48 85 C0",
        },
    },
    {
        "3.5.0",
        {
            "E8 C8 AD 3F 00",
            "4C 8D 05 09 08 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 0B BC 00 00 48 85 C0",
        },
    },
    {
        "3.5.1",
        {
            "E8 AE 4D 3F 00 84 DB",
            "4C 8D 05 09 08 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 0B BC 00 00 48 85 C0",
        },
    },
    {
        "3.6.0",
        {
            "E8 FC 8F 41 00 E8 C7 AD 22 04",
            "4C 8D 05 F9 07 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 EB BD 00 00 48 85 C0",
        },
    },
    {
        "3.6.1",
        {
            "E8 AC 90 41 00 E8 B7 AA 22 04",
            "4C 8D 05 F9 07 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 EB BD 00 00 48 85 C0",
        },
    },
    {
        "3.6.2",
        {
            "E8 7C 9C 41 00 E8 47 BC 22 04",
            "4C 8D 05 F9 07 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 EB BD 00 00 48 85 C0",
        },
    },
    {
        "3.6.4",
        {
            "E8 5C 9D 41 00 E8",
            "4C 8D 05 09 08 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 EB BD 00 00 48 85 C0",
        },
    },
    {
        "3.6.5",
        {
            "E8 1C A0 41 00 E8",
            "4C 8D 05 09 08 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 EB BD 00 00 48 85 C0",
        },
    },
#pragma endregion // Blender 3.x

#pragma region Blender 4.x
    {
        "4.0.0",
        {
            "E8 A9 4E 45 00",
            "4C 8D 05 09 0A 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 FB 26 00 00 48 85 C0",
        },
    },
    {
        "4.0.1",
        {
            "E8 89 4E 45 00",
            "4C 8D 05 09 0A 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 FB 26 00 00 48 85 C0",
        },
    },
    {
        "4.0.2",
        {
            "E8 89 54 45 00",
            "4C 8D 05 09 0A 00 00",
            "E8 7B FF FF FF 84 C0",
            "E8 FB 26 00 00 48 85 C0",
        },
    }
#pragma endregion // Blender 4.x
};
