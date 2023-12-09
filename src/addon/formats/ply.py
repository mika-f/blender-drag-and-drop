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
    FloatProperty,  # pyright: ignore[reportUnknownVariableType]
)
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportPLYWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_ply_with_defaults"
    bl_label = "Import PLY File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.ply_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportPLYWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_ply_with_custom_settings"
    bl_label = "Import PLY File"

    # Properties based on Blender v4.0.0 (ordered by parameters on documents)
    global_scale: FloatProperty(default=1.0, min=1e-06, max=1e06, name="Scale")
    use_scene_unit: BoolProperty(default=False, name="Scene Unit")
    forward_axis: EnumProperty(
        default="Y",
        name="Forward Axis",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("NEGATIVE_X", "-X", ""),
            ("NEGATIVE_Y", "-Y", ""),
            ("NEGATIVE_Z", "-Z", ""),
        ],
    )
    up_axis: EnumProperty(
        default="Z",
        name="Up Axis",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("NEGATIVE_X", "-X", ""),
            ("NEGATIVE_Y", "-Y", ""),
            ("NEGATIVE_Z", "-Z", ""),
        ],
    )
    merge_verts: BoolProperty(default=False, name="Merge Vertices")
    import_colors: EnumProperty(
        default="SRGB",
        name="Import Vertex Colors",
        items=[("NONE", "None", ""), ("SRGB", "sRGB", ""), ("LINEAR", "Linear", "")],
    )

    def draw(self, context: Context):
        column = self.get_column()
        column.prop(self, "global_scale")
        column.prop(self, "use_scene_unit")
        column.prop(self, "forward_axis")
        column.prop(self, "up_axis")
        column.prop(self, "merge_verts")
        column.prop(self, "import_colors")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.ply_import(
            filepath=self.filepath(),
            global_scale=self.global_scale,
            use_scene_unit=self.use_scene_unit,
            forward_axis=self.forward_axis,
            up_axis=self.up_axis,
            merge_verts=self.merge_verts,
            import_colors=self.import_colors,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_PLY(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Polygon File Format File"

    def format(self):
        return "ply"


OPERATORS = [
    ImportPLYWithDefaults,
    ImportPLYWithCustomSettings,
    VIEW3D_MT_Space_Import_PLY,
]
