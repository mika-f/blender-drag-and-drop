# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownMemberType=false

import bpy

from bpy.props import FloatProperty  # type: ignore
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class Import3MFWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_3mf_with_defaults"
    bl_label = "Import 3D Manufacturing Format File"

    def execute(self, context: Context):
        bpy.ops.import_mesh.threemf(filepath=self.filepath())
        return {"FINISHED"}


class Import3MFWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_3mf_with_custom_settings"
    bl_label = "Import 3D Manufacturing Format File with Custom Settings"

    # properties
    # ref: https://github.com/Ghostkeeper/Blender3mfFormat/tree/v1.0.2
    global_scale: FloatProperty(default=1.0, min=0.0001, max=1000, name="Global Scale")

    def draw(self, context: Context):
        box = self.layout.box()
        column = box.column()

        column.use_property_split = True

        column.prop(self, "global_scale")

    def execute(self, context: Context):
        bpy.ops.import_mesh.threemf(
            filepath=self.filepath(),
            global_scale=self.global_scale,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_3MF(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import  3D Manufacturing Format File"

    @staticmethod
    def format():
        return "3mf"


OPERATORS = [
    Import3MFWithDefaults,
    Import3MFWithCustomSettings,
    VIEW3D_MT_Space_Import_3MF,
]
