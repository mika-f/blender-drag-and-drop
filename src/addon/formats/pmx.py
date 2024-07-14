# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportInvalidTypeForm=false

from typing import Set
import bpy

from bpy.props import (
    BoolProperty,  # pyright: ignore[reportUnknownVariableType]
    EnumProperty,  # pyright: ignore[reportUnknownVariableType]
    FloatProperty,  # pyright: ignore[reportUnknownVariableType]
    IntProperty,  # pyright: ignore[reportUnknownVariableType]
)
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


def include_types(cls, _):  # type: ignore
    types = cls.types.copy()  # type: ignore

    if "PHYSICS" in types:
        types.add("ARMATURE")
    if "DISPLAY" in types:
        types.add("ARMATURE")
    if "MORPHS" in types:
        types.add("ARMATURE")
        types.add("MESH")

    if types != cls.types:
        cls.types = types


class ImportPMXWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_pmx_with_defaults"
    bl_label = "Import MikuMikuDance Model File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.mmd_tools.import_model(filepath=self.filepath())
        return {"FINISHED"}


class ImportPMXWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_pmx_with_custom_settings"
    bl_label = "Import MikuMikuDance Model File"

    # Properties based on MMD Tools 2.x
    # https://github.com/UuuNyaa/blender_mmd_tools/blob/d148bdbd520a0ddb2ffd0389a0217a297ad107f0/mmd_tools/operators/fileio.py#L62
    types: EnumProperty(
        default={
            "MESH",
            "ARMATURE",
            "PHYSICS",
            "DISPLAY",
            "MORPHS",
        },
        name="Types",
        items=[
            ("MESH", "Mesh", "Mesh", 1),
            ("ARMATURE", "Armature", "Armature", 2),
            ("PHYSICS", "Physics", "Rigidbodies and joints (include Armature)", 4),
            ("DISPLAY", "Display", "Display frames (include Armature)", 8),
            ("MORPHS", "Morphs", "Morphs (include Armature and Mesh)", 16),
        ],  # type: ignore
        options={"ENUM_FLAG"},
        update=include_types,
    )
    scale: FloatProperty(default=0.08, min=1e-06, max=1e06, name="Scale")
    clean_model: BoolProperty(
        default=True,
        name="Clean Model",
        description="Remove unused vertices, materials, and textures",
    )
    remove_doubles: BoolProperty(
        default=True,
        name="Remove Doubles",
        description="Merge duplicated vertices and faces",
    )
    fix_IK_links: BoolProperty(
        default=False,
        name="Fix IK Links",
        description="Fix IK links to be Blender suitable",
    )
    ik_loop_factor: IntProperty(
        default=5,
        min=1,
        soft_max=10,
        max=100,
        name="IK Loop Factor",
        description="Scaling factor of MMD IK loop",
    )
    apply_bone_fixed_axis: BoolProperty(
        default=False,
        name="Apply Bone Fixed Axis",
        description="Apply bone's fixed axis to be Blender Suitable",
    )
    rename_bones: BoolProperty(
        default=True,
        name="Rename Bones - L / R Suffix",
        description="Use Blender naming convention for Left / Right paired bones",
    )
    use_underscore: BoolProperty(
        default=False,
        name="Rename Bones - Use Underscore",
        description="Will not use dot, e.g. if renaming bones, will use _R instead of .R",
    )
    # dictionary: EnumProperty() # NOT SUPPORTED YET IN Drag-and-Drop Support
    use_mipmap: BoolProperty(
        default=True,
        name="Use MIP maps for UV textures",
        description="Specify if mipmaps will be generated",
    )
    sph_blend_factor: FloatProperty(
        default=1.0,
        name="Influence of .sph textures",
        description="The diffuse color factor of texture slot for .sph textures",
    )
    spa_blend_factor: FloatProperty(
        default=1.0,
        name="Influence of .spa textures",
        description="The specular color factor of texture slot for .spa textures",
    )

    def draw(self, context: Context):
        column = self.get_column()
        column.prop(self, "types")
        column.prop(self, "scale")
        column.prop(self, "clean_model")
        column.prop(self, "remove_doubles")
        column.prop(self, "fix_IK_links")
        column.prop(self, "ik_loop_factor")
        column.prop(self, "apply_bone_fixed_axis")
        column.prop(self, "rename_bones")
        column.prop(self, "use_underscore")
        column.prop(self, "use_mipmap")
        column.prop(self, "sph_blend_factor")
        column.prop(self, "spa_blend_factor")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.mmd_tools.import_model(
            filepath=self.filepath(),
            types=self.types,
            scale=self.scale,
            clean_model=self.clean_model,
            remove_doubles=self.remove_doubles,
            fix_IK_links=self.fix_IK_links,
            ik_loop_factor=self.ik_loop_factor,
            apply_bone_fixed_axis=self.apply_bone_fixed_axis,
            rename_LR_bones=self.rename_bones,
            use_underscore=self.use_underscore,
            use_mipmap=self.use_mipmap,
            sph_blend_factor=self.sph_blend_factor,
            spa_blend_factor=self.spa_blend_factor,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_PMD(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import MikuMikuDance Model File"

    @staticmethod
    def format():
        return "pmd"


class VIEW3D_MT_Space_Import_PMX(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import MikuMikuDance Model File"

    @staticmethod
    def format():
        return "pmx"


OPERATORS = [
    ImportPMXWithDefaults,
    ImportPMXWithCustomSettings,
    VIEW3D_MT_Space_Import_PMD,
    VIEW3D_MT_Space_Import_PMX,
]
