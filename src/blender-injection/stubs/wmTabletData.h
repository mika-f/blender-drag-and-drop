#pragma once


using wmTabletData = struct wmTabletData
{
    int active;
    float pressure;
    float x_tilt;
    float y_tilt;
    char is_motion_absolute;
};
