# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

from __future__ import annotations

from bpy.props import BoolProperty  # pyright: ignore[reportUnknownVariableType]
from bpy.types import AddonPreferences, Context

from . import interop

items: list[str] = [
    "This addon uses C++ DLL code. Please check DLL publisher and DO NOT replace it.",
    "The C++ DLL hooks calls to certain functions in Blender.exe in order to receive events on drop.",
    " This is the desired behavior as Blender itself does not provide any events for drops.",
    "If you disable the add-on, these behaviors are restored.",
]


class DragAndDropPreferences(AddonPreferences):
    bl_idname = __package__

    def callback(self, context: Context):
        interop.try_load()
        pass

    is_accept: BoolProperty(name="Accept", default=False, update=callback)

    def draw(self, context: Context):
        layout = self.layout
        column = layout.column()

        column.label(
            text="Please check the following sections before using this addon:"
        )

        for i, label in enumerate(items):
            column.label(text=f"{i+1}. {label}")

        column.prop(
            self,
            "is_accept",
            text="Using this addon with an understanding of the above",
        )

        return
