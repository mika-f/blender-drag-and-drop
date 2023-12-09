#pragma once
#include <unordered_map>
#include <Windows.h>

#include "BlenderPatchPatterns.h"

struct BlenderPatch
{
private:
    // patch byte patterns
    BlenderPatchPattern* _patterns;

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
    BlenderPatch(BlenderPatchPattern* patterns) : _patterns(patterns)
    {
        StoreMemoryPointers(
            _patterns->get_bpy_interface_BPY_run_string_eval(),
            _patterns->get_space_view3d_view3d_ima_empty_drop_poll(),
            _patterns->get_space_view3d_view3d_ima_drop_poll(),
            _patterns->get_view3d_select_ED_view3d_give_object_under_cursor()
        );
    }

    [[nodiscard]] std::uintptr_t Get_view3d_ima_empty_drop_poll() const;

    void BPY_run_string_eval(void* c, const char* imports[], const char* expression) const;

    bool view3d_ima_drop_poll(void* c, void* drag, void* event) const;

    void* ED_view3d_give_object_under_cursor(void*, int [2]) const;
};
