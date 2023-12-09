# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

from __future__ import annotations

import bpy
import os
import typing

from bpy.props import StringProperty  # pyright: ignore[reportUnknownVariableType]
from bpy.types import Context, Event, Operator

from .formats.super import VIEW3D_MT_Space_Import_BASE

# formats that Blender does not supported by default
conditionals: typing.Dict[str, typing.Callable[[], bool]] = {
    "vrm": lambda: hasattr(bpy.ops.import_scene, "vrm"),
}


class DropEventListener(Operator):
    bl_idname = "object.drop_event_listener"
    bl_label = "Open File via Drag and Drop"

    filename: StringProperty()  # type: ignore

    def inflate(self, name: str):
        VIEW3D_MT_Space_Import_BASE.filename = self.filename  # type: ignore
        bpy.ops.wm.call_menu(name=name)  # type: ignore
        return

    def invoke(self, context: Context, event: Event):
        try:
            path = typing.cast(str, self.filename)  # type: ignore
            _, ext = os.path.splitext(path)

            if ext[1:].lower() in conditionals:
                if not conditionals[ext[1:].lower()]():
                    return {"FINISHED"}

            # dynamically called importer
            name = f"VIEW3D_MT_Space_Import_{ext[1:].upper()}"
            self.inflate(name)
        except TypeError as e:
            print(e)
        except RuntimeError as e:
            print(e)

        return {"FINISHED"}
