# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

from typing import Set
import bpy

from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportSVGWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_svg_with_defaults"
    bl_label = "Import SVG File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.import_curve.svg(filepath=self.filepath())
        return {"FINISHED"}


class ImportSVGWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_svg_with_custom_settings"
    bl_label = "Import SVG File"

    def draw(self, context: Context):
        pass

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.import_curve.svg(filepath=self.filepath())
        return {"FINISHED"}


class VIEW3D_MT_Space_Import_SVG(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import SVG File"

    def format(self):
        return "svg"


OPERATORS = [
    ImportSVGWithDefaults,
    ImportSVGWithCustomSettings,
    VIEW3D_MT_Space_Import_SVG,
]
