#include "pch.h"

#include "BlenderObj.h"
#include "BlenderPatcher.h"

const std::vector<std::string> SUPPORTED_FORMATS = {
    ".abc",
    ".bvh",
    ".fbx",
    ".dae",
    ".glb",
    ".gltf",
    ".obj",
    ".ply",
    ".stl",
    ".svg",
    ".usd",
    ".usda",
    ".usdc",
    ".x3d",
    ".wrl"
};

std::unordered_map<std::uintptr_t, bool> onFired = {};

extern "C" void DropEventHookCallback(void* c, void* win, char* path)
{
    std::cout << "f:" << path << std::endl;
}

extern "C" bool View3DImaEmptyDropPollHookCallback(void* c, wmDrag* drag, void* event)
{
    const std::filesystem::path path(drag->path);
    const auto extension = path.extension();

    const auto ref = std::ranges::find(SUPPORTED_FORMATS, extension);
    if (ref != std::end(SUPPORTED_FORMATS))
    {
        const auto ptr = reinterpret_cast<std::intptr_t>(drag);
        if (onFired.contains(ptr))
        {
            return false;
        }

        onFired[ptr] = true;

        const char* imports[] = {"bpy", nullptr};
        const auto expression = R"(bpy.ops.object.drop_event_listener2("INVOKE_DEFAULT", filename=R")" + std::string(drag->path) + "\")";

        BlenderPatcher::GetInstance()->RunStringEval(c, imports, expression.c_str());
    }

    return false;
}

extern "C" bool view3d_ima_drop_poll(void* c, void* drag, void* event)
{
    return BlenderPatcher::GetInstance()->View3DImaDropPoll(c, drag, event);
}

extern "C" void* ED_view3d_give_object_under_cursor(void* c, int mvals[2])
{
    return BlenderPatcher::GetInstance()->EDView3dGiveObjectUnderCursor(c, mvals);
}
