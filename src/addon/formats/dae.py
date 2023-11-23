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
    IntProperty,  # pyright: ignore[reportUnknownVariableType]
)
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportDAEWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_dae_with_defaults"
    bl_label = "Import DAE File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.collada_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportDAEWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_dae_with_custom_settings"
    bl_label = "Import DAE File"

    # Properties based on Blender v4.0.0 (ordered by parameters on documents)
    import_units: BoolProperty(default=False, name="Import Units")
    custom_normals: BoolProperty(default=True, name="Custom Normals")
    fix_orientation: BoolProperty(default=False, name="Fix Leaf Bones")
    find_chains: BoolProperty(default=False, name="Find Bone Chains")
    auto_connect: BoolProperty(default=False, name="Auto Connect")
    min_chain_length: IntProperty(default=0, name="Minimum Chain Length")
    keep_bind_info: BoolProperty(default=False, name="Keep Bind Info")

    import_data_options_section: BoolProperty(default=True, name="Import Data Options")
    armature_options_section: BoolProperty(default=True, name="Armature Options")

    def draw(self, context: Context):
        # Import Data Options Section
        column, state = self.get_expand_column("import_data_options_section")
        if state:
            column.prop(self, "import_units")
            column.prop(self, "custom_normals")

        # Armature Options Section
        column, state = self.get_expand_column("armature_options_section")
        if state:
            column.prop(self, "fix_orientation")
            column.prop(self, "find_chains")
            column.prop(self, "auto_connect")
            column.prop(self, "min_chain_length")

        column = self.get_column()
        column.prop(self, "keep_bind_info")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.wm.collada_import(
            filepath=self.filepath(),
            import_units=self.import_units,
            custom_normals=self.custom_normals,
            fix_orientation=self.fix_orientation,
            find_chains=self.find_chains,
            auto_connect=self.auto_connect,
            min_chain_length=self.min_chain_length,
            keep_bind_info=self.keep_bind_info,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_DAE(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Collada File"

    def format(self):
        return "dae"


OPERATORS = [
    ImportDAEWithDefaults,
    ImportDAEWithCustomSettings,
    VIEW3D_MT_Space_Import_DAE,
]
