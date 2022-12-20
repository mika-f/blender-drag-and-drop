#include "pch.h"

#include "BlenderPatcher.h"
#include "BlenderPatch.h"
#include "extern.h"
#include "strings.h"

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

void BlenderPatcher::ApplyInjector() 
{
    const auto patch = GetPatch();
    if (patch.GetPatchVersion() == PatchVersion::PatchToDropEvent)
    {
        const auto address = patch.Get_view3d_ima_empty_drop_poll();
        constexpr auto bytes = 96;
        unsigned char assembly[bytes];

        this->GetAssemblyCodeFrom(address, &assembly, bytes);

        std::vector<unsigned char> vector;

        for (int i = 0; i < bytes; i++)
            vector.push_back(assembly[i]);

        this->_originals[address] = vector;

        this->ReplaceFunctionWithCall(address, reinterpret_cast<void*>(&View3DImaEmptyDropPollHook), bytes);

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

void BlenderPatcher::RestoreInjector()
{
    const auto patch = GetPatch();
    if (patch.GetPatchVersion() == PatchVersion::PatchToDropEvent)
    {
        const auto address = patch.Get_view3d_ima_empty_drop_poll();
        auto assembly = this->_originals[address];
        unsigned char* arr = &assembly[0];

        Injector::WriteMemoryRaw(address, arr, assembly.size(), true);
    }
}


void BlenderPatcher::GetAssemblyCodeFrom(const Injector::memory_pointer_tr& at, void* ret, unsigned int bytes) const
{
    ReadMemoryRaw(at, ret, bytes, true);
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

void BlenderPatcher::UnPatch()
{
    try
    {
        this->RestoreInjector();
    }
    catch (std::out_of_range&)
    {
        std::cout << "[ERROR] exception: out of range" << std::endl;
        std::cout << "[ERROR] injector detected the unsupported version of Blender. Please upgrade Drag-and-Drop Support or downgrade Blender" << std::endl;
        std::cout << "[ERROR] detected version : " << this->_version << std::endl;
    }
}


bool BlenderPatcher::View3DImaDropPoll(void* c, void* drag, void* event) const
{
    return this->GetPatch().view3d_ima_drop_poll(c, drag, event);
}

void* BlenderPatcher::EDView3dGiveObjectUnderCursor(void* c, int mvals[2]) const
{
    return this->GetPatch().ED_view3d_give_object_under_cursor(c, mvals);
}

void BlenderPatcher::RunStringEval(void* c, const char* imports[], const char* expression) const
{
    this->GetPatch().BPY_run_string_eval(c, imports, expression);
}
