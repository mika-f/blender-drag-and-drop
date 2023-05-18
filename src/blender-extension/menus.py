# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------


import bpy

from bpy.types import Context


class VIEW3D_MT_Space_Import_BASE(bpy.types.Menu):
    filename: str

    def draw(self, context: Context | None):
        layout = self.layout

        col = layout.column()
        col.operator(
            f"object.import_{self.format()}_with_defaults", text="Import with Defaults"
        ).filename = VIEW3D_MT_Space_Import_BASE.filename  # type: ignore

        col = layout.column()
        col.operator_context = "INVOKE_DEFAULT"
        col.operator(
            f"object.import_{self.format()}_with_custom_settings",
            text="Import with Custom Settings",
        ).filename = VIEW3D_MT_Space_Import_BASE.filename  # type: ignore

    def format(self) -> str:
        return ""


class VIEW3D_MT_Space_Import_ABC(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Alembic File"

    def format(self):
        return "abc"


class VIEW3D_MT_Space_Import_BVH(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Biovision Hierarchy File"

    def format(self):
        return "bvh"


class VIEW3D_MT_Space_Import_DAE(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Collada File"

    def format(self):
        return "dae"


class VIEW3D_MT_Space_Import_FBX(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import FBX File"

    def format(self):
        return "fbx"


class VIEW3D_MT_Space_Import_GLB(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import glTF File"

    def format(self):
        return "glb"


class VIEW3D_MT_Space_Import_GLTF(VIEW3D_MT_Space_Import_GLB):
    pass


class VIEW3D_MT_Space_Import_OBJ(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Wavefront OBJ File"

    def format(self):
        return "obj"


class VIEW3D_MT_Space_Import_PLY(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Polygon File Format File"

    def format(self):
        return "ply"


class VIEW3D_MT_Space_Import_STL(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Standard Triangulated Language File"

    def format(self):
        return "stl"


class VIEW3D_MT_Space_Import_SVG(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Scalable Vector Graphics File"

    def format(self):
        return "svg"


class VIEW3D_MT_Space_Import_USD(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    def format(self):
        return "usd"


class VIEW3D_MT_Space_Import_USDA(VIEW3D_MT_Space_Import_USD):
    pass


class VIEW3D_MT_Space_Import_USDC(VIEW3D_MT_Space_Import_USD):
    pass


class VIEW3D_MT_Space_Import_VRM(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Virtual Reality Model File"

    def format(self):
        return "vrm"


class VIEW3D_MT_Space_Import_X3D(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Extensible 3D File Format File"

    def format(self):
        return "x3d"


class VIEW3D_MT_Space_Import_WRL(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import WRL File"

    def format(self):
        return "x3d"
