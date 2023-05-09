#include "pch.h"

#include "BlenderObj.h"
#include "BlenderPatcher.h"

std::vector<std::intptr_t> isAlreadyTriggered = {};

extern "C" void DropEventHookCallback(void* c, void* win, char* path)
{
    std::cout << "f:" << path << std::endl;
}

extern "C" bool View3DImaEmptyDropPollHookCallback(bContext* c, wmDrag* drag, wmEvent* event)
{
    const auto ptr = reinterpret_cast<intptr_t>(drag);

    if (BlenderPatcher::GetInstance()->View3DImaDropPoll(c, drag, event))
    {
        auto ob = static_cast<int*>(BlenderPatcher::GetInstance()->EDView3dGiveObjectUnderCursor(c, event->mval));
        if (ob == nullptr)
            return true;

        // NOTE: the pointed fields (value) have been determined, this cast is no problem.
        if (reinterpret_cast<int>(ob + 0x000000E0) == /* OB_EMPTY */ 0 && reinterpret_cast<int>(ob + 0x000003FF) == /* OB_EMPTY_IMAGE */ 8) // NOLINT(clang-diagnostic-pointer-to-int-cast)
            return true;
    }

    if (drag->type == /* WM_DRAG_PATH */ 4)
    {
        const std::filesystem::path path(drag->path);
        const auto extension = path.extension();

        if (const auto itr = std::ranges::find(isAlreadyTriggered, ptr); itr != std::end(isAlreadyTriggered))
            return false; // already triggered

        isAlreadyTriggered.push_back(ptr);

        const char* imports[] = {"bpy", nullptr};
        const auto expression = R"(bpy.ops.object.drop_event_listener("INVOKE_DEFAULT", filename=R")" + std::string(drag->path) + "\")";

        BlenderPatcher::GetInstance()->RunStringEval(c, imports, expression.c_str());
        return false; // already triggered

    }


    return false;
}
