#include "pch.h"

#include "BlenderObj.h"
#include "BlenderPatcher.h"

std::vector<std::intptr_t> isAlreadyTriggered = {};

const char* GetDropFilePath(void* pUnknown)
{
    if (BlenderPatcher::GetInstance()->GetVersion() >= std::make_tuple(3, 6, 0))
    {
        const auto drag = static_cast<wmDrag360*>(pUnknown);
        const auto pointer = static_cast<wmDragPath*>(drag->poin);
        return pointer->path;
    }

    const auto drag = static_cast<wmDrag*>(pUnknown);
    return drag->path;
}

bool ShouldTriggerDropEvent(const char* w)
{
    return true; // always true
}

bool IsEventAlreadyTriggered(void* drag)
{
    const auto ptr = reinterpret_cast<intptr_t>(drag);
    if (const auto itr = std::ranges::find(isAlreadyTriggered, ptr); itr != std::end(isAlreadyTriggered))
        return true;
    return false;
}

bool TriggerDropEvent(bContext* c, const char* path, void* ptr)
{
    isAlreadyTriggered.push_back(reinterpret_cast<intptr_t>(ptr));

    const char* imports[] = {"bpy", nullptr};
    const auto expression = R"(bpy.ops.object.drop_event_listener("INVOKE_DEFAULT", filename=R")" + std::string(path) + "\")";

    BlenderPatcher::GetInstance()->RunStringEval(c, imports, expression.c_str());
    return false; // already triggered
}

extern "C" void DropEventHookCallback(void* c, void* win, char* path)
{
    std::cout << "f:" << path << std::endl;
}

// static bool view3d_ima_empty_drop_poll(bContext *C, wmDrag *drag, const wmEvent *event)
extern "C" bool View3DImaEmptyDropPollHookCallback(bContext* c, wmDrag* drag, wmEvent* event)
{
    const auto ptr = reinterpret_cast<intptr_t>(drag);

    if (drag->type == /* WM_DRAG_PATH */4)
    {
        if (const auto path = GetDropFilePath(drag); ShouldTriggerDropEvent(path))
        {
            if (BlenderPatcher::GetInstance()->GetVersion() >= std::make_tuple(4, 0, 0))
            {
                if (event->val != 0)
                    return false;
            }
            else
            {
                if (IsEventAlreadyTriggered(event))
                    return false;
            }

            return TriggerDropEvent(c, path, drag);
        }
    }

    if (!BlenderPatcher::GetInstance()->View3DImaDropPoll(c, drag, event))
        return false;

    auto ob = static_cast<int*>(BlenderPatcher::GetInstance()->EDView3dGiveObjectUnderCursor(c, event->mval));
    if (ob == nullptr)
        return true;

    // NOTE: the pointed fields (value) have been determined, this cast is no problem.
    if (reinterpret_cast<int>(ob + 0x000000E0) == /* OB_EMPTY */ 0 && reinterpret_cast<int>(ob + 0x000003FF) == /* OB_EMPTY_IMAGE */ 8) // NOLINT(clang-diagnostic-pointer-to-int-cast)
        return true;

    return false;
}
