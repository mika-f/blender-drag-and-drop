#include "pch.h"

#include <filesystem>

#include "BlenderPatcher.h"
#include "BlenderObj.h"
#include "BlenderPatch.h"
#include "strings.h"

const std::vector<std::string> SupportedFormats = {
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

extern "C" bool View3DImaEmptyDropPollHookCallback(Context* c, wmDrag* drag, wmEvent* event)
{
    const std::filesystem::path path(drag->path);
    const auto extension = path.extension();

    const auto ref = std::ranges::find(SupportedFormats, extension);
    if (ref != std::end(SupportedFormats))
    {
        const auto ptr = reinterpret_cast<std::intptr_t>(drag);
        if (onFired.contains(ptr))
        {
            return false;
        }

        onFired[ptr] = true;

        const char* imports[] = {"bpy", nullptr};
        const auto expression = "bpy.ops.object.drop_event_listener2(\"INVOKE_DEFAULT\", filename=R\"" + std::string(drag->path) + "\")";

        BlenderPatcher::GetInstance()->RunStringEval(c, imports, expression.c_str());
    }

    return false;
}

extern "C" bool view3d_ima_drop_poll(Context* c, wmDrag* drag, wmEvent* event)
{
    return BlenderPatcher::GetInstance()->View3DImaDropPoll(c, drag, event);
}

extern "C" void* ED_view3d_give_object_under_cursor(Context* c, int mvals[2])
{
    return BlenderPatcher::GetInstance()->EDView3dGiveObjectUnderCursor(c, mvals);
}

void BlenderPatcher::FetchVersion()
{
    TCHAR filename[MAX_PATH + 1];

    GetModuleFileName(nullptr, filename, sizeof(filename));

    const auto size = GetFileVersionInfoSize(filename, nullptr);

    if (const auto version = new BYTE[size]; GetFileVersionInfo(filename, NULL, size, version))
    {
        unsigned int len;
        VS_FIXEDFILEINFO* pFileInfo;

        VerQueryValue(version, "\\", reinterpret_cast<void**>(&pFileInfo), &len);

        this->_version = format("%d.%d.%d", HIWORD(pFileInfo->dwFileVersionMS), LOWORD(pFileInfo->dwFileVersionMS), HIWORD(pFileInfo->dwFileVersionLS));
    }
}

BlenderPatch BlenderPatcher::GetPatch() const
{
    return Patchers.at(this->_version);
}

void BlenderPatcher::ApplyInjector() const
{
    const auto patch = GetPatch();
    if (patch.GetPatchVersion() == PatchVersion::PatchToDropEvent)
    {
        const auto address = patch.Get_view3d_ima_empty_drop_poll();
        this->ReplaceFunctionWithCall(address, reinterpret_cast<void*>(&View3DImaEmptyDropPollHook), 96);

        return;
    }

    if (patch.GetPatchVersion() == PatchVersion::PatchToPrintF)
    {
        const auto instance = &BytePattern::temp_instance();
        instance->find_pattern(this->_pattern);

        if (instance->count() > 0)
        {
            const auto address = instance->get_first().address();
            this->ReplaceInstructionWithCall(address, reinterpret_cast<void*>(&DropEventHook));

            return;
        }
    }

    std::cout << "[ERROR] failed to patch to Blender because injector does not support " << this->_version << " currently" << std::endl;
}

void BlenderPatcher::ReplaceInstructionWithCall(const Injector::memory_pointer_tr& at, void* dest, bool ret) const
{
    unsigned char assembly[] = {
        /* MOV  RAX, 0000000000000000h */ 0x48, 0xB8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        /* CALL RAX                    */ 0xFF, 0xD0,
    };

    *reinterpret_cast<void**>(&assembly[2]) = dest;

    WriteMemoryRaw(at, assembly, sizeof(assembly), true);

    if (ret)
    {
        Injector::WriteMemory<uint8_t>(at + 12, 0xC3, true);
    }
}

void BlenderPatcher::ReplaceFunctionWithCall(const Injector::memory_pointer_tr& at, void* dest, unsigned int paddings) const
{
    unsigned char assembly[] = {
        /* MOV  RAX, 0000000000000000h */ 0x48, 0xB8, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        /* JMP  RAX                    */ 0xFF, 0xE0,
    };

    *reinterpret_cast<void**>(&assembly[2]) = dest;

    WriteMemoryRaw(at, assembly, sizeof(assembly), true);

    constexpr auto len = sizeof(assembly);
    if (len >= paddings)
    {
        return;
    }

    for (unsigned int i = len; i < paddings; i++)
    {
        Injector::WriteMemory<uint8_t>(at + i, 0xCC, true);
    }
}


// public
BlenderPatcher* BlenderPatcher::GetInstance()
{
    if (!_instance)
    {
        _instance = new BlenderPatcher();
    }

    return _instance;
}


void BlenderPatcher::Patch()
{
    try
    {
        this->FetchVersion();
        this->ApplyInjector();
    }
    catch (std::out_of_range&)
    {
        std::cout << "[ERROR] exception: out of range" << std::endl;
        std::cout << "[ERROR] injector detected the unsupported version of Blender. Please upgrade Drag-and-Drop Support or downgrade Blender" << std::endl;
        std::cout << "[ERROR] detected version : " << this->_version << std::endl;
    }
}

bool BlenderPatcher::View3DImaDropPoll(Context* c, wmDrag* drag, wmEvent* event) const
{
    return this->GetPatch().view3d_ima_drop_poll(c, drag, event);
}

void* BlenderPatcher::EDView3dGiveObjectUnderCursor(Context* c, int mvals[2]) const
{
    return this->GetPatch().ED_view3d_give_object_under_cursor(c, mvals);
}

void BlenderPatcher::RunStringEval(void* c, const char* imports[], const char* expression) const
{
    this->GetPatch().BPY_run_string_eval(c, imports, expression);
}
