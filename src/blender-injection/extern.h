#pragma once


extern "C" void DropEventHook(const char*, char*);

extern "C" bool View3DImaEmptyDropPollHook(void*, void*, void*);

extern "C" bool view3d_ima_drop_poll(void*, void*, void*);

extern "C" void* ED_view3d_give_object_under_cursor(void*, int [2]);
