# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

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


class ImportFBXWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_fbx_with_defaults"
    bl_label = "Import FBX File"

    def execute(self, context: Context):
        bpy.ops.import_scene.fbx(filepath=self.filepath())
        return {"FINISHED"}


class ImportFBXWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_fbx_with_custom_settings"
    bl_label = "Import FBX File"

    # Properties based on Blender latest (ordered by parameters on documents)
    use_manual_orientation: BoolProperty(default=False, name="Manual Orientation")
    global_scale: FloatProperty(default=1.0, name="Global Scale", min=0.001, max=1000)
    bake_space_transform: BoolProperty(default=False, name="Apply Transform")
    use_custom_normals: BoolProperty(default=True, name="Custom Normals")
    use_image_search: BoolProperty(default=True, name="Image Search")
    use_alpha_decals: BoolProperty(default=False, name="Alpha Decals")
    decal_offset: FloatProperty(default=0.0, name="Decal Offset", min=0, max=1)
    use_anim: BoolProperty(default=True, name="Animation")
    anim_offset: FloatProperty(default=1.0, name="Animation Offset")
    use_subsurf: BoolProperty(default=False, name="Subdivision Data")
    use_custom_props: BoolProperty(default=True, name="Custom Properties")
    use_custom_props_enum_as_string: BoolProperty(
        default=True, name="Import Enums As Strings"
    )
    ignore_leaf_bones: BoolProperty(default=False, name="Ignore Leaf Bones")
    force_connect_children: BoolProperty(default=False, name="Force Connect Children")
    automatic_bone_orientation: BoolProperty(
        default=False, name="Automatic Bone Orientation"
    )
    primary_bone_axis: EnumProperty(
        default="Y",
        name="Primary Bone Axis",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )
    secondary_bone_axis: EnumProperty(
        default="X",
        name="Secondary Bone Axis",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )
    use_prepost_rot: BoolProperty(default=True, name="Use Pre/Post Rotation")
    axis_forward: EnumProperty(
        default="-Z",
        name="Axis Forward",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )
    axis_up: EnumProperty(
        default="Y",
        name="Axis Up",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )

    # added by Blender 3.4
    colors_type: EnumProperty(
        default="SRGB",
        name="Vertex Colors",
        items=[("NONE", "None", ""), ("SRGB", "sRGB", ""), ("LINEAR", "Linear", "")],
    )

    # ui properties
    include_section: BoolProperty(default=True, name="Include")
    transform_section: BoolProperty(default=True, name="Transform")
    animation_section: BoolProperty(default=True, name="Animation")
    armature_section: BoolProperty(default=True, name="Armature")

    def draw(self, context: Context):
        # Include Section
        column, state = self.get_expand_column("include_section")

        if state:
            column.prop(self, "use_custom_normals")
            column.prop(self, "use_subsurf")
            column.prop(self, "use_custom_props")
            column.prop(self, "use_custom_props_enum_as_string")
            column.prop(self, "use_image_search")

            if bpy.app.version >= (3, 4, 0):
                column.prop(self, "colors_type")

        # Transform Section
        column, state = self.get_expand_column("transform_section")

        if state:
            column.prop(self, "global_scale")
            column.prop(self, "decal_offset")

            row = column.row()
            row.prop(self, "bake_space_transform")
            row.label(text="", icon="ERROR")

            column.prop(self, "use_prepost_rot")
            column.prop(self, "use_manual_orientation")

            orientation = column.column()
            orientation.enabled = self.use_manual_orientation
            orientation.prop(self, "axis_forward")
            orientation.prop(self, "axis_up")

        # Animation Section
        column, state = self.get_expand_column("animation_section")

        if state:
            column.prop(self, "use_anim")

            animation = column.column()
            animation.enabled = self.use_anim
            animation.prop(self, "anim_offset")

        # Armature Section
        column, state = self.get_expand_column("armature_section")

        if state:
            column.prop(self, "ignore_leaf_bones")
            column.prop(self, "force_connect_children")
            column.prop(self, "automatic_bone_orientation")
            column.prop(self, "primary_bone_axis")
            column.prop(self, "secondary_bone_axis")

    def execute(self, context: Context):
        bpy.ops.import_scene.fbx(
            filepath=self.filepath(),
            use_manual_orientation=self.use_manual_orientation,
            global_scale=self.global_scale,
            bake_space_transform=self.bake_space_transform,
            use_custom_normals=self.use_custom_normals,
            colors_type=self.colors_type,
            use_image_search=self.use_image_search,
            use_alpha_decals=self.use_alpha_decals,
            decal_offset=self.decal_offset,
            use_anim=self.use_anim,
            anim_offset=self.anim_offset,
            use_subsurf=self.use_subsurf,
            use_custom_props=self.use_custom_props,
            use_custom_props_enum_as_string=self.use_custom_props_enum_as_string,
            ignore_leaf_bones=self.ignore_leaf_bones,
            force_connect_children=self.force_connect_children,
            automatic_bone_orientation=self.automatic_bone_orientation,
            primary_bone_axis=self.primary_bone_axis,
            secondary_bone_axis=self.secondary_bone_axis,
            use_prepost_rot=self.use_prepost_rot,
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_FBX(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import FBX File"

    def format(self):
        return "fbx"


OPERATORS = [
    ImportFBXWithDefaults,
    ImportFBXWithCustomSettings,
    VIEW3D_MT_Space_Import_FBX,
]
