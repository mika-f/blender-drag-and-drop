#pragma once

#include "eWM_EventFlag.h"
#include "wmTabletData.h"

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
  void *customdata;
  short prev_type;
  short prev_val;
  int prev_xy[2];
  short prev_press_type;
  int prev_press_xy[2];
  uint8_t prev_press_modifier;
  short prev_press_keymodifier;
  double prev_press_time;
};
