# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false


import bpy.ops

from typing import cast
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportImageWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_image_with_defaults"
    bl_label = "Import PNG File"

    def execute(self, context: Context):

        bpy.ops.object.empty_add(
            type="IMAGE",
            align="VIEW",
            location=context.scene.cursor.location,
            scale=(5, 5, 5),
        )

        empty = bpy.context.active_object

        bpy.ops.image.open(filepath=self.filepath())
        img = self.find_opened_image(self.filepath())

        if img is not None:
            empty.data = img

        return {"FINISHED"}

    def find_opened_image(self, path: str) -> bpy.types.Image | None:
        for (
            item
        ) in bpy.data.images.items():  # pyright: ignore[reportUnknownVariableType]
            i = cast(bpy.types.Image, item[1])  # pyright: ignore[reportInvalidTypeForm]

            if i.filepath == path:
                return i


class VIEW3D_MT_Space_Import_BMP(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import BMP File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_BW(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Iris File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_CIN(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Cineon & DPX File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_DPX(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Cineon & DPX File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_EXR(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import OpenEXR File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_HDR(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import HDR File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_J2C(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import JPEG 2000 File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_JP2(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import JPEG 2000 File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_JPG(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import JPEG File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_JPEG(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import JPEG File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_PNG(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import PNG File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_RGB(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Iris File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_SGI(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Iris File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_TIF(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import TIFF File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_TIFF(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import TIFF File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_TGA(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Targa File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


class VIEW3D_MT_Space_Import_WEBP(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import WebP File"

    @staticmethod
    def format():
        return "image"

    @staticmethod
    def has_custom_importer() -> bool:
        return False


OPERATORS = [
    ImportImageWithDefaults,
    VIEW3D_MT_Space_Import_BMP,
    VIEW3D_MT_Space_Import_BW,
    VIEW3D_MT_Space_Import_CIN,
    VIEW3D_MT_Space_Import_DPX,
    VIEW3D_MT_Space_Import_EXR,
    VIEW3D_MT_Space_Import_HDR,
    VIEW3D_MT_Space_Import_J2C,
    VIEW3D_MT_Space_Import_JP2,
    VIEW3D_MT_Space_Import_JPG,
    VIEW3D_MT_Space_Import_JPEG,
    VIEW3D_MT_Space_Import_PNG,
    VIEW3D_MT_Space_Import_RGB,
    VIEW3D_MT_Space_Import_SGI,
    VIEW3D_MT_Space_Import_TIF,
    VIEW3D_MT_Space_Import_TIFF,
    VIEW3D_MT_Space_Import_TGA,
    VIEW3D_MT_Space_Import_WEBP,
]
