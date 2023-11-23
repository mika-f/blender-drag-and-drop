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


class ImportBVHWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_bvh_with_defaults"
    bl_label = "Import BVH File"

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.import_anim.bvh(filepath=self.filepath())
        return {"FINISHED"}


class ImportBVHWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_bvh_with_custom_settings"
    bl_label = "Import BVH File"

    # Properties based on Blender v4.0.0 (ordered by parameters on documents)
    target: EnumProperty(
        default="ARMATURE",
        name="Target",
        items=[("ARMATURE", "Armature", ""), ("OBJECT", "Object", "")],
    )
    global_scale: FloatProperty(default=1.0, min=0.0001, max=1e06, name="Scale")
    frame_start: IntProperty(default=1, name="Start Frame")
    use_fps_scale: BoolProperty(default=False, name="Scale FPS")
    update_scene_fps: BoolProperty(default=False, name="Update Scene FPS")
    update_scene_duration: BoolProperty(default=False, name="Update Scene Duration")
    use_cyclic: BoolProperty(default=False, name="Loop")
    rotate_mode: EnumProperty(
        default="NATIVE",
        name="Rotation",
        items=[
            ("QUATERNION", "Quaternion", ""),
            ("NATIVE", "Euler (Native)", ""),
            ("XYZ", "Euler (XYZ)", ""),
            ("XZY", "Euler (XZY)", ""),
            ("YXZ", "Euler (YXZ)", ""),
            ("YZX", "Euler (YZX)", ""),
            ("ZXY", "Euler (ZXY)", ""),
            ("ZYX", "Euler (ZYX)", ""),
        ],
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
            ("X", "X Forward", ""),
            ("Y", "Y Forward", ""),
            ("Z", "Z Forward", ""),
            ("-X", "-X Forward", ""),
            ("-Y", "-Y Forward", ""),
            ("-Z", "-Z Forward", ""),
        ],
    )

    transform_section: BoolProperty(default=True, name="Transform")
    animation_section: BoolProperty(default=True, name="Animation")

    def draw(self, context: Context):
        column = self.get_column()
        column.prop(self, "target")

        # Transform Section
        column, state = self.get_expand_column("transform_section")
        if state:
            column.prop(self, "global_scale")
            column.prop(self, "rotate_mode")
            column.prop(self, "axis_forward")
            column.prop(self, "axis_up")

        # Animation Section
        column, state = self.get_expand_column("animation_section")
        if state:
            column.prop(self, "frame_start")
            column.prop(self, "use_fps_scale")
            column.prop(self, "use_cyclic")
            column.prop(self, "update_scene_fps")
            column.prop(self, "update_scene_duration")

    def execute(self, context: Context) -> Set[str] | Set[int]:
        bpy.ops.import_anim.bvh(
            filepath=self.filepath(),
            target=self.target,
            global_scale=self.global_scale,
            frame_start=self.frame_start,
            use_fps_scale=self.use_fps_scale,
            update_scene_fps=self.update_scene_fps,
            update_scene_duration=self.update_scene_duration,
            use_cyclic=self.use_cyclic,
            rotate_mode=self.rotate_mode,
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_BVH(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Biovision Hierarchy File"

    def format(self):
        return "bvh"


OPERATORS = [
    ImportBVHWithDefaults,
    ImportBVHWithCustomSettings,
    VIEW3D_MT_Space_Import_BVH,
]
