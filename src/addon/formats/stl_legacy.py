# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

import bpy

from bpy.props import BoolProperty, EnumProperty, FloatProperty  # type: ignore
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportSTLLegacyWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_stl_legacy_with_defaults"
    bl_label = "Import Wavefront STL File"

    def execute(self, context: Context):
        bpy.ops.import_mesh.stl(filepath=self.filepath())
        return {"FINISHED"}


class ImportSTLLegacyWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_stl_legacy_with_custom_settings"
    bl_label = "Import Wavefront STL File"

    # deprecated properties (>= 3.4.0)
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

    transform_section: BoolProperty(default=True, name="Transform")
    geometry_section: BoolProperty(default=True, name="Geometry")

    def draw(self, context: Context):
        # Transform Section
        column, state = self.get_expand_column("transform_section")
        if state:
            column.prop(self, "global_scale")
            column.prop(self, "use_scene_unit")
            column.prop(self, "axis_forward")
            column.prop(self, "axis_up")

        # Geometry Section
        column, state = self.get_expand_column("geometry")
        if state:
            column.prop(self, "use_facet_normal")

    def execute(self, context: Context):
        bpy.ops.import_mesh.stl(
            global_scale=self.global_scale,
            use_scene_unit=self.use_scene_unit,
            use_facet_normal=self.use_facet_normal,
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_STLLegacy(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Wavefront STL File"

    def format(self):
        return "stl"


OPERATORS = [
    ImportSTLLegacyWithDefaults,
    ImportSTLLegacyWithCustomSettings,
    VIEW3D_MT_Space_Import_STLLegacy,
]
