# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownMemberType=false

import bpy

from bpy.props import BoolProperty, EnumProperty  # type: ignore
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportGLBWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_glb_with_defaults"
    bl_label = "Import GLB File"

    def execute(self, context: Context):
        bpy.ops.import_scene.gltf(filepath=self.filepath())
        return {"FINISHED"}


class ImportGLBWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_glb_with_custom_settings"
    bl_label = "Import GLB File"

    convert_lighting_mode: EnumProperty(
        default="SPEC",
        name="Lighting Mode",
        items=[
            ("SPEC", "Standard", ""),
            ("COMPAT", "Unitless", ""),
            ("RAW", "Raw (Deprecated)", ""),
        ],
    )
    import_pack_images: BoolProperty(default=True, name="Pack Images")
    merge_vertices: BoolProperty(default=False, name="Merge Vertices")
    import_shading: EnumProperty(
        default="NORMALS",
        name="Shading",
        items=[
            ("NORMALS", "Use Normal Data", ""),
            ("FLAT", "Flat Shading", ""),
            ("SMOOTH", "Smooth Shading", ""),
        ],
    )
    bone_heuristic: EnumProperty(
        default="TEMPERANCE",
        name="Bone Dir",
        items=[
            ("BLENDER", "Blender (best for re-importing)", ""),
            ("TEMPERANCE", "Temperance (average)", ""),
            ("FORTUNE", "Fortune (may look better, less accurate)", ""),
        ],
    )
    guess_original_bind_pose: BoolProperty(
        default=True, name="Guess Original Bind Pose"
    )

    def draw(self, context: Context):
        box = self.layout.box()
        column = box.column()

        column.use_property_split = True

        column.prop(self, "import_pack_images")
        column.prop(self, "merge_vertices")
        column.prop(self, "import_shading")
        column.prop(self, "guess_original_bind_pose")
        column.prop(self, "bone_heuristic")

        if bpy.app.version >= (3, 4, 0):
            column.prop(self, "convert_lighting_mode")

    def execute(self, context: Context):
        bpy.ops.import_scene.gltf(
            filepath=self.filepath(),
            convert_lighting_mode=self.convert_lighting_mode,
            import_pack_images=self.import_pack_images,
            merge_vertices=self.merge_vertices,
            import_shading=self.import_shading,
            bone_heuristic=self.bone_heuristic,
            guess_original_bind_pose=self.guess_original_bind_pose,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_GLB(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import glTF File"

    def format(self):
        return "glb"


class VIEW3D_MT_Space_Import_GLTF(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import glTF File"

    def format(self):
        return "glb"


OPERATORS = [
    ImportGLBWithDefaults,
    ImportGLBWithCustomSettings,
    VIEW3D_MT_Space_Import_GLB,
    VIEW3D_MT_Space_Import_GLTF,
]
