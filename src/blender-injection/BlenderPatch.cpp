#include "pch.h"

#include "BlenderPatch.h"
#include "strings.h"


std::uintptr_t BlenderPatch::GetInjectionLocationFor(std::string instruction)
{
    const auto instance = &BytePattern::temp_instance();
    instance->find_pattern(instruction);

    if (instance->count() == 1)
    {
        return instance->get_first().address();
    }

    return reinterpret_cast<uintptr_t>(nullptr);
}

std::intptr_t BlenderPatch::GetRelativeOffsetFor(std::string instruction) const
{
    const auto instructions = split(instruction, ' ');

    if (instruction.starts_with("4C 8D 05") || instruction.starts_with("4C 8D 0D"))
    {
        // first 3bytes are op-code, after 4 bytes are load address
        // LEA  R8, [RIP+...]
        // LEA  R9, [RIP+...]
        std::string hex;

        for (auto i = 3; i < 3 + 4; i++)
            hex.insert(0, instructions[i]);

        const auto rel = strtol(hex.c_str(), nullptr, 16);
        return rel + 7;
    }

    if (instruction.starts_with("E8") || instruction.starts_with("E9"))
    {
        // first 1 byte is op-code, after 4 bytes are jump address
        // CALL ...
        // JMP  ...
        // CALL/JMP to address adding 5 bytes

        std::string hex;
        auto hasSign = false;

        for (auto i = 1; i < 1 + 4; i++)
            hex.insert(0, instructions[i]);

        // add 0xFFFFFFFF, it will minus
        if ('8' <= hex[0])
        {
            hasSign = true;
            hex.insert(0, "0x");
        }

        const auto rel = std::stoll(hex.c_str(), nullptr, 16);
        return (hasSign ? (rel - 0x100000000L) : rel) + 5;
    }

    return reinterpret_cast<intptr_t>(nullptr);
}


/**
 * supported instructions:
 *
 * LEA  R8, [RIP+...]    : 0x4C, 0x8D, 0x05, ...
 * LEA  R9, [RIP+...]    : 0x4C, 0x8D, 0x0D, ...
 * CALL ...              : 0xE8, ...
 * JMP  ...              : 0xE9, ...
 */
std::uintptr_t BlenderPatch::GetFunctionPointerFor(std::string instruction) const
{
    const auto cur = GetInjectionLocationFor(instruction);
    const auto off = GetRelativeOffsetFor(instruction);

    return cur + off;
}

template <class... TArgs>
void BlenderPatch::StoreMemoryPointers(TArgs... args)
{
    for (std::string instruction : std::initializer_list<std::string>{args...})
    {
        this->_dict[instruction] = this->GetFunctionPointerFor(instruction);
    }
}

template <class TReturn, class... TArgs>
TReturn BlenderPatch::InvokeFunction(std::string instruction, TArgs... args) const
{
    const void* pointer = Injector::memory_pointer_tr(this->_dict.at(instruction)).get();
    const auto func = reinterpret_cast<TReturn(*)(TArgs...)>(pointer);
    return func(args...);
}


// public

PatchVersion BlenderPatch::GetPatchVersion() const
{
    return this->_version;
}

std::uintptr_t BlenderPatch::Get_view3d_ima_empty_drop_poll() const
{
    if (this->GetPatchVersion() != PatchVersion::PatchToDropEvent)
        return reinterpret_cast<uintptr_t>(nullptr);
    return _dict.at(this->_space_view3d_view3d_ima_empty_drop_poll);
}


void BlenderPatch::BPY_run_string_eval(void* c, const char* imports[], const char* expression) const
{
    if (this->GetPatchVersion() != PatchVersion::PatchToDropEvent)
        return;

    this->InvokeFunction<void, void*, const char*[], const char*>(this->_bpy_interface_BPY_run_string_eval, c, imports, expression);
}

bool BlenderPatch::view3d_ima_drop_poll(void* c, void* drag, void* event) const
{
    if (this->GetPatchVersion() != PatchVersion::PatchToDropEvent)
        return reinterpret_cast<std::uintptr_t>(nullptr);

    return this->InvokeFunction<bool, void*, void*, void*>(this->_space_view3d_view3d_ima_drop_poll, c, drag, event);
}

void* BlenderPatch::ED_view3d_give_object_under_cursor(void* c, int mvals[2]) const
{
    if (this->GetPatchVersion() != PatchVersion::PatchToDropEvent)
        return (nullptr);

    return this->InvokeFunction<void*, void*, int[2]>(this->_view3d_select_ED_view3d_give_object_under_cursor, c, mvals);
}
