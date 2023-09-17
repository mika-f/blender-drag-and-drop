# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownMemberType=false

import bpy

from bpy.props import BoolProperty  # type: ignore
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportVRMWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_vrm_with_defaults"
    bl_label = "Import VRM File"

    def execute(self, context: Context):
        bpy.ops.import_scene.vrm(filepath=self.filepath())
        return {"FINISHED"}


class ImportVRMWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_vrm_with_custom_settings"
    bl_label = "Import VRM File with Custom Settings"

    # properties
    # ref: https://github.com/saturday06/VRM-Addon-for-Blender/blob/d15fc0070835e9b9ec7622817691a89d52fceab7/io_scene_vrm/importer/import_scene.py#L73-L100
    extract_textures_into_folder: BoolProperty(
        default=False, name="Extract texture images into the folder"
    )
    make_new_texture_folder: BoolProperty(
        default=True, name="Don't overwrite existing texture folder (limit:100,000)"
    )
    set_shading_type_to_material_on_import: BoolProperty(
        default=True, name='Set shading type to "Material"'
    )
    set_view_transform_to_standard_on_import: BoolProperty(
        default=True, name='Set view transform to "Standard"'
    )
    set_armature_display_to_wire: BoolProperty(
        default=True, name='Set an imported armature display to "Wire"'
    )
    set_armature_display_to_show_in_front: BoolProperty(
        default=True, name='Set an imported armature display to show "In-Front"'
    )

    def draw(self, context: Context):
        box = self.layout.box()
        column = box.column()

        column.use_property_split = True

        column.prop(self, "extract_textures_into_folder")
        column.prop(self, "make_new_texture_folder")
        column.prop(self, "set_shading_type_to_material_on_import")
        column.prop(self, "set_view_transform_to_standard_on_import")
        column.prop(self, "set_armature_display_to_wire")
        column.prop(self, "set_armature_display_to_show_in_front")

    def execute(self, context: Context):
        bpy.ops.import_scene.vrm(
            filepath=self.filepath(),
            extract_textures_into_folder=self.extract_textures_into_folder,
            make_new_texture_folder=self.make_new_texture_folder,
            set_shading_type_to_material_on_import=self.set_shading_type_to_material_on_import,
            set_view_transform_to_standard_on_import=self.set_view_transform_to_standard_on_import,
            set_armature_display_to_wire=self.set_armature_display_to_wire,
            set_armature_display_to_show_in_front=self.set_armature_display_to_show_in_front,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_VRM(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Virtual Reality Model File"

    def format(self):
        return "vrm"


OPERATORS = [
    ImportVRMWithDefaults,
    ImportVRMWithCustomSettings,
    VIEW3D_MT_Space_Import_VRM,
]
