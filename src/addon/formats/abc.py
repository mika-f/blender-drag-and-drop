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
    FloatProperty,  # pyright: ignore[reportUnknownVariableType]
)
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportABCWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_abc_with_defaults"
    bl_label = "Import ABC File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.alembic_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportABCWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_abc_with_custom_settings"
    bl_label = "Import ABC File"

    # Properties based on Blender v4.0.0 (ordered by parameters on documents)
    relative_path: BoolProperty(default=True, name="Relative Path")
    scale: FloatProperty(default=1.0, min=0.0001, max=1000, name="Scale")
    set_frame_range: BoolProperty(default=True, name="Set Frame Range")
    validate_meshes: BoolProperty(default=False, name="Validate Meshes")
    always_add_cache_reader: BoolProperty(default=False, name="Always Add Cache Reader")
    is_sequence: BoolProperty(default=False, name="Is Sequence")

    manual_transform_section: BoolProperty(default=True, name="Manual Transform")
    options_section: BoolProperty(default=True, name="Option")

    def draw(self, context: Context):
        # Manual Transform Section
        column, state = self.get_expand_column("manual_transform_section")

        if state:
            column.prop(self, "scale")

        # Options Section
        column, state = self.get_expand_column("options_section")

        if state:
            column.prop(self, "relative_path")
            column.prop(self, "set_frame_range")
            column.prop(self, "is_sequence")
            column.prop(self, "validate_meshes")
            column.prop(self, "always_add_cache_reader")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.alembic_import(
            filepath=self.filepath(),
            relative_path=self.relative_path,
            scale=self.scale,
            set_frame_range=self.set_frame_range,
            validate_meshes=self.validate_meshes,
            always_add_cache_reader=self.always_add_cache_reader,
            is_sequence=self.is_sequence,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_ABC(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import ABC File"

    def format(self):
        return "abc"


OPERATORS = [
    ImportABCWithDefaults,
    ImportABCWithCustomSettings,
    VIEW3D_MT_Space_Import_ABC,
]
