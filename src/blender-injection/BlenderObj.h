#pragma once

// define memory layouts of Blender

struct bContext
{
    int thread;

    struct
    {
        void* manager;
        void* window;
        void* workspace;
        void* screen;
        void* area;
        void* region;
        void* menu;
        void* gizmo_group;
        void* store;

        const char* operator_poll_msg;

        struct PollMsgDyn_Params
        {
            char* (*get_fn)(bContext*, void*);
            char* (*free_fn)(bContext*, void*);
            void* user_data;
        } operator_poll_msg_dyn_params;
    } wm;

    struct
    {
        void* main;
        void* scene;
        int recursion;
        bool py_init;
        void* py_context;
        void* py_context_orig;
    } data;
};

using eWM_DragFlags = enum eWM_DragFlags
{
    WM_DRAG_NOP = 0,
    WM_DRAG_FREE_DATA = 1,
};

using ListBase = struct ListBase
{
    void *first, *last;
};

using wmDragActiveDropState = struct wmDragActiveDropState
{
    struct wmDropBox* active_dropbox;
    struct ScrArea* area_from;
    struct ARegion* region_from;
    struct bContextStore* ui_context;
    const char* disabled_info;
    bool free_disabled_info;
};

using wmDrag = struct wmDrag
{
    struct wmDrag *next, *prev;
    int icon;
    int type;
    void* poin;
    char path[1024];
    double value;
    struct ImBuf* imb;
    float imbuf_scale;
    wmDragActiveDropState drop_state;
    eWM_DragFlags flags;
    ListBase ids;
    ListBase asset_items;
};

using wmTabletData = struct wmTabletData
{
    int active;
    float pressure;
    float x_tilt;
    float y_tilt;
    char is_motion_absolute;
};

using eWM_EventFlag = enum eWM_EventFlag
{
    WM_EVENT_SCROLL_INVERT = (1 << 0),
    WM_EVENT_IS_REPEAT = (1 << 1),
    WM_EVENT_FORCE_DRAG_THRESHOLD = (1 << 2),
};

using wmEvent = struct wmEvent
{
    struct wmEvent *next, *prev;
    short type;
    short val;
    int xy[2];
    int mval[2];
    char utf8_buf[6];
    uint8_t modifier;
    int8_t direction;
    short keymodifier;
    wmTabletData tablet;
    eWM_EventFlag flag;
    short custom;
    short customdata_free;
    void* customdata;
    short prev_type;
    short prev_val;
    int prev_xy[2];
    short prev_press_type;
    int prev_press_xy[2];
    uint8_t prev_press_modifier;
    short prev_press_keymodifier;
    double prev_press_time;
};
