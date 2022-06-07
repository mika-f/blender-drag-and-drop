# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

from bpy.types import Panel

from .operator import DropEventListener


class DropEventListenerUI(Panel):
    bl_idname = "UI_PT_DropEventListener"
    bl_label = "Drag and Drop Support"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        cls = DropEventListener
        layout = self.layout

        if not cls.is_listening():
            layout.operator(cls.bl_idname, text="Start Listening", icon="PLAY")
        else:
            layout.operator(cls.bl_idname, text="Stop Listening", icon="PAUSE")
