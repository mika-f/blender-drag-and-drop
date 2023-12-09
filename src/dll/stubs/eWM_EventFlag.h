#pragma once

using eWM_EventFlag = enum eWM_EventFlag {
  WM_EVENT_SCROLL_INVERT = (1 << 0),
  WM_EVENT_IS_REPEAT = (1 << 1),
  WM_EVENT_FORCE_DRAG_THRESHOLD = (1 << 2),
};
