# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

from typing import Set
import bpy
from bpy.props import (
    BoolProperty,  # pyright: ignore[reportUnknownVariableType]
    EnumProperty,  # pyright: ignore[reportUnknownVariableType]
)
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportX3DWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_x3d_with_defaults"
    bl_label = "Import X3D File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.import_scene.x3d(filepath=self.filepath())
        return {"FINISHED"}


class ImportX3DWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_x3d_with_custom_settings"
    bl_label = "Import X3D File"

    axis_forward: EnumProperty(
        default="Y",
        name="Forward",
        items=[
            ("X", "X Forward", ""),
            ("Y", "Y Forward", ""),
            ("Z", "Z Forward", ""),
            ("-X", "-X Forward", ""),
            ("-Y", "-Y Forward", ""),
            ("-Z", "-Z Forward", ""),
        ],
    )
    axis_up: EnumProperty(
        default="Z",
        name="Up",
        items=[
            ("X", "X Up", ""),
            ("Y", "Y Up", ""),
            ("Z", "Z Up", ""),
            ("-X", "-X Up", ""),
            ("-Y", "-Y Up", ""),
            ("-Z", "-Z Up", ""),
        ],
    )

    transform_section: BoolProperty(default=True, name="Transform")

    def draw(self, context: Context):
        column, state = self.get_expand_column("transform")
        if state:
            column.prop(self, "axis_forward")
            column.prop(self, "axis_up")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.import_scene.x3d(
            filepath=self.filepath(),
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_X3D(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Extensible 3D File Format File"

    def format(self):
        return "x3d"


class VIEW3D_MT_Space_Import_WRL(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import WRL File"

    def format(self):
        return "x3d"


OPERATORS = [
    ImportX3DWithDefaults,
    ImportX3DWithCustomSettings,
    VIEW3D_MT_Space_Import_X3D,
    VIEW3D_MT_Space_Import_WRL,
]
