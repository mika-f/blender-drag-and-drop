#pragma once
#include "ListBase.h"
#include "eWM_DragDataType.h"
#include "eWM_DragFlags.h"
#include "wmDragActiveDropState.h"

// Blender < 3.6.0
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

// Blender >= 3.6.0
using wmDrag360 = struct wmDrag360
{
    struct wmDrag *next, *prev;
    int icon;
    eWM_DragDataType type;
    void* poin;
    double value;

    /** If no icon but imbuf should be drawn around cursor. */
    const struct ImBuf* imb;
    float imbuf_scale;

    wmDragActiveDropState drop_state;

    eWM_DragFlags flags;

    /** List of wmDragIDs, all are guaranteed to have the same ID type. */
    ListBase ids;
    /** List of `wmDragAssetListItem`s. */
    ListBase asset_items;
};
