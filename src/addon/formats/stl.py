# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportInvalidTypeForm=false

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


class ImportSTLWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_stl_with_defaults"
    bl_label = "Import Wavefront STL File (Experimental)"

    def execute(self, context: Context):
        bpy.ops.wm.stl_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportSTLWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_stl_with_custom_settings"
    bl_label = "Import Wavefront STL File (Experimental)"

    global_scale: FloatProperty(default=1.0, min=1e-06, max=1e06, name="Scale")
    use_scene_unit: BoolProperty(default=False, name="Scene Unit")
    use_facet_normal: BoolProperty(default=False, name="Facet Normals")
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
    use_mesh_validate: BoolProperty(default=False, name="Validate Mesh")

    def draw(self, context: Context):
        column = self.get_column()
        column.prop(self, "global_scale")
        column.prop(self, "use_scene_unit")
        column.prop(self, "axis_forward")
        column.prop(self, "axis_up")
        column.prop(self, "use_facet_normal")

    def execute(self, context: Context):
        bpy.ops.wm.stl_import(
            global_scale=self.global_scale,
            use_scene_unit=self.use_scene_unit,
            use_facet_normal=self.use_facet_normal,
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
            use_mesh_validate=self.use_mesh_validate,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_STL(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Wavefront STL File (Experimental)"

    @staticmethod
    def format():
        return "stl"


class VIEW3D_FH_Import_STL(bpy.types.FileHandler):
    bl_idname = "VIEW3D_FH_Import_STL"
    bl_label = "Import Wavefront STL File (Experimental)"
    bl_import_operator = "object.drop_event_listener"
    bl_file_extensions = ".stl"

    @classmethod
    def poll_drop(cls, context: bpy.types.Context | None) -> bool:
        if context is None:
            return False
        return context and context.area and context.area.type == "VIEW_3D"


OPERATORS: list[type] = [
    ImportSTLWithDefaults,
    ImportSTLWithCustomSettings,
    VIEW3D_MT_Space_Import_STL,
    VIEW3D_FH_Import_STL,
]
