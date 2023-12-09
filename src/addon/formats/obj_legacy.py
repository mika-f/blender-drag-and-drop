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


class ImportOBJLegacyWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_obj_legacy_with_defaults"
    bl_label = "Import Wavefront OBJ File"

    def execute(self, context: Context):
        bpy.ops.import_scene.obj(filepath=self.filepath())
        return {"FINISHED"}


class ImportOBJLegacyWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_obj_legacy_with_custom_settings"
    bl_label = "Import Wavefront OBJ File"

    # deprecated properties (>= 3.4.0)
    use_edges: BoolProperty(default=True, name="Lines")
    use_smooth_groups: BoolProperty(default=True, name="Smooth Groups")
    use_split_objects: BoolProperty(default=True, name="Split by Object")
    use_split_groups: BoolProperty(default=False, name="Split by Group")
    use_groups_as_vgroups: BoolProperty(default=False, name="Poly Groups")
    use_image_search: BoolProperty(default=True, name="Image Search")
    split_mode: EnumProperty(
        default="ON",
        name="Split",
        items=[
            ("ON", "Split", ""),
            ("OFF", "Keep Vert Order", ""),
        ],
    )
    global_clamp_size: FloatProperty(
        default=0.0, name="Clamp Size", min=0.0, max=1000.0
    )
    axis_forward: EnumProperty(
        default="-Z",
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
        default="Y",
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

    # ui properties
    include_section: BoolProperty(default=True, name="Include")
    transform_section: BoolProperty(default=True, name="Transform")
    geometry_section: BoolProperty(default=True, name="Geometry")

    def draw(self, context: Context):
        # Include Section
        column, state = self.get_expand_column("include_section")

        if state:
            column.prop(self, "use_image_search")
            column.prop(self, "use_smooth_groups")
            column.prop(self, "use_edges")

        # Transform Section
        column, state = self.get_expand_column("transform_section")

        if state:
            column.prop(self, "global_clamp_size")
            column.prop(self, "axis_forward")
            column.prop(self, "axis_up")

        # Geometry Section
        column, state = self.get_expand_column("geometry_section")

        if state:
            row = column.row()
            row.prop(self, "split_mode", expand=True)

            if self.split_mode == "ON":
                column.prop(self, "use_split_objects")
                column.prop(self, "use_split_groups")
            else:
                column.prop(self, "use_groups_as_vgroups")

    def execute(self, context: Context):
        bpy.ops.import_scene.obj(
            filepath=self.filepath(),
            use_edges=self.use_edges,
            use_smooth_groups=self.use_smooth_groups,
            use_split_objects=self.use_split_objects,
            use_split_groups=self.use_split_groups,
            use_groups_as_vgroups=self.use_groups_as_vgroups,
            use_image_search=self.use_image_search,
            split_mode=self.split_mode,
            global_clamp_size=self.global_clamp_size,
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_OBJLegacy(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Wavefront OBJ File"

    def format(self):
        return "obj"


OPERATORS = [
    ImportOBJLegacyWithDefaults,
    ImportOBJLegacyWithCustomSettings,
    VIEW3D_MT_Space_Import_OBJLegacy,
]
