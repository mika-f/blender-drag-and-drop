#pragma once

#include "BlenderPatch.h"

#pragma comment(lib, "version.lib")

class BlenderPatcher
{
private:
    std::string _version;

    std::unordered_map<std::uintptr_t, std::vector<unsigned char>> _originals;

    BlenderPatch* _patch = nullptr;

    inline static BlenderPatcher* _instance = nullptr;

    BlenderPatcher()
    {
        this->_version = "0.0.0";
    }

    void FetchVersion();
    void ApplyInjector();
    void RestoreInjector();
    void GetAssemblyCodeFrom(const Injector::memory_pointer_tr& at, void* ret, unsigned int bytes) const;
    void ReplaceInstructionWithCall(const Injector::memory_pointer_tr& at, void* dest, bool ret = false) const;
    void ReplaceFunctionWithCall(const Injector::memory_pointer_tr& at, void* dest, unsigned int paddings = 0) const;

public:
    static BlenderPatcher* GetInstance();

    void Patch();
    void UnPatch();

    bool View3DImaDropPoll(void* c, void* drag, void* event) const;
    void* EDView3dGiveObjectUnderCursor(void* c, int mvals[2]) const;
    void RunStringEval(void* c, const char* imports[], const char* expression) const;
};

bool LaunchDebugger();
