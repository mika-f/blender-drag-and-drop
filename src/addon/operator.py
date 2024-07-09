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

from .formats import CLASSES
from .formats.super import VIEW3D_MT_Space_Import_BASE

# formats that Blender does not supported by default
conditionals: typing.Dict[str, typing.Callable[[], bool]] = {
    "3mf": lambda: hasattr(bpy.ops.import_mesh, "threemf"),
    "vrm": lambda: hasattr(bpy.ops.import_scene, "vrm"),
}

operators: list[type] = []


class DropEventListener(Operator):
    bl_idname = "object.drop_event_listener"
    bl_label = "Open File via Drag and Drop"

    filename: StringProperty()  # type: ignore

    def find_class(self, ext: str) -> VIEW3D_MT_Space_Import_BASE | None:
        for c in CLASSES:
            if c.__name__ == f"VIEW3D_MT_Space_Import_{ext}":
                return typing.cast(VIEW3D_MT_Space_Import_BASE, c)

    def inflate(self, name: str, ext: str):
        VIEW3D_MT_Space_Import_BASE.filename = self.filename  # type: ignore

        c = self.find_class(ext)
        if c is None:
            return  # invalid operation

        if c.has_custom_importer():
            bpy.ops.wm.call_menu(name=name)  # type: ignore
        else:
            i = getattr(bpy.ops.object, f"import_{c.format()}_with_defaults")
            if i is not None:
                print(i)
                i("EXEC_DEFAULT", filename=self.filename)
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
            self.inflate(name, ext[1:].upper())
        except TypeError as e:
            print(e)
        except RuntimeError as e:
            print(e)

        return {"FINISHED"}

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return context.area and context.area.type == "VIEW_3D"


operators.append(DropEventListener)


def get_operators():
    return operators
