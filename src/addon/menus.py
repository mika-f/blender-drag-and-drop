# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------


from .formats.super import VIEW3D_MT_Space_Import_BASE


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


class VIEW3D_MT_Space_Import_X3D(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Extensible 3D File Format File"

    def format(self):
        return "x3d"


class VIEW3D_MT_Space_Import_WRL(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import WRL File"

    def format(self):
        return "x3d"
