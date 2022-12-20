#pragma once

// define memory layouts of Blender

struct Context
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
            char* (*get_fn)(Context*, void*);
            char* (*free_fn)(Context*, void*);
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
    /** Informs which dropbox is activated with the drag item.
     * When this value changes, the #draw_activate and #draw_deactivate dropbox callbacks are
     * triggered.
     */
    struct wmDropBox* active_dropbox;

    /** If `active_dropbox` is set, the area it successfully polled in. To restore the context of it
     * as needed. */
    struct ScrArea* area_from;
    /** If `active_dropbox` is set, the region it successfully polled in. To restore the context of
     * it as needed. */
    struct ARegion* region_from;

    /** If `active_dropbox` is set, additional context provided by the active (i.e. hovered) button.
     * Activated before context sensitive operations (polling, drawing, dropping). */
    struct bContextStore* ui_context;

    /** Text to show when a dropbox poll succeeds (so the dropbox itself is available) but the
     * operator poll fails. Typically the message the operator set with
     * CTX_wm_operator_poll_msg_set(). */
    const char* disabled_info;
    bool free_disabled_info;
};

using wmDrag = struct wmDrag
{
    struct wmDrag *next, *prev;

    int icon;
    /** See 'WM_DRAG_' defines above. */
    int type;
    void* poin;
    char path[1024]; /* FILE_MAX */
    double value;

    /** If no icon but imbuf should be drawn around cursor. */
    struct ImBuf* imb;
    float imbuf_scale;

    wmDragActiveDropState drop_state;

    eWM_DragFlags flags;

    /** List of wmDragIDs, all are guaranteed to have the same ID type. */
    ListBase ids;
    /** List of `wmDragAssetListItem`s. */
    ListBase asset_items;
};
