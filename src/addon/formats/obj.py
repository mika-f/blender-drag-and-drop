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


class ImportOBJWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_obj_with_defaults"
    bl_label = "Import Wavefront OBJ File"

    def execute(self, context: Context):
        bpy.ops.wm.obj_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportOBJWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_obj_with_custom_settings"
    bl_label = "Import Wavefront OBJ File"

    # properties
    global_scale: FloatProperty(default=1.0, name="Scale", min=0.0001, max=10000)
    clamp_size: FloatProperty(default=0.0, name="Clamp Bounding Box", min=0, max=1000)
    forward_axis: EnumProperty(
        name="Forward Axis",
        default="-Z",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )
    up_axis: EnumProperty(
        name="Up Axis",
        default="Y",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )
    use_split_objects: BoolProperty(default=True, name="Split by Object")
    use_split_groups: BoolProperty(default=False, name="Split by Group")
    import_vertex_groups: BoolProperty(default=False, name="Vertex Groups")
    validate_meshes: BoolProperty(default=False, name="Validate Meshes")

    # ui properties
    transform_section: BoolProperty(default=True, name="Transform")
    options_section: BoolProperty(default=True, name="Options")

    def draw(self, context: Context):
        # Transform Section
        column, state = self.get_expand_column("transform_section")

        if state:
            column.prop(self, "global_scale")
            column.prop(self, "clamp_size")
            column.prop(self, "forward_axis")
            column.prop(self, "up_axis")

        # Options Section
        column, state = self.get_expand_column("options_section")

        if state:
            column.prop(self, "use_split_objects")
            column.prop(self, "use_split_groups")
            column.prop(self, "import_vertex_groups")
            column.prop(self, "validate_meshes")

    def execute(self, context: Context):
        bpy.ops.wm.obj_import(
            filepath=self.filepath(),
            global_scale=self.global_scale,
            clamp_size=self.clamp_size,
            forward_axis=self.forward_axis,
            up_axis=self.up_axis,
            use_split_objects=self.use_split_objects,
            use_split_groups=self.use_split_groups,
            import_vertex_groups=self.import_vertex_groups,
            validate_meshes=self.validate_meshes,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_OBJ(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Wavefront OBJ File"

    def format(self):
        return "obj"


OPERATORS = [
    ImportOBJWithDefaults,
    ImportOBJWithCustomSettings,
    VIEW3D_MT_Space_Import_OBJ,
]
