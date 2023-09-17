#pragma once

using wmDragActiveDropState = struct wmDragActiveDropState
{
    struct wmDropBox* active_dropbox;
    struct ScrArea* area_from;
    struct ARegion* region_from;
    struct bContextStore* ui_context;
    const char* disabled_info;
    bool free_disabled_info;
};
