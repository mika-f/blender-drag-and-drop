# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the GPLv3 License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false
# pyright: reportInvalidTypeForm=false

import os
import bpy

from bpy.props import BoolProperty, EnumProperty  # type: ignore
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportDXFWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_dxf_with_defaults"
    bl_label = "Import AutoCAD DXF File"

    def execute(self, context: Context):
        # Ensure the built-in DXF extension is enabled
        if not hasattr(bpy.ops.import_scene, 'dxf'):
            try:
                bpy.ops.preferences.addon_enable(module="io_import_dxf")
            except Exception:
                pass
                
        # The official DXF importer requires 'directory' and 'files' collection
        # rather than just a single 'filepath' string, because it loops over self.files.
        filepath = self.filepath()
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
                
        bpy.ops.import_scene.dxf(
            'EXEC_DEFAULT',
            filepath=filepath,
            directory=directory,
            files=[{'name': filename}]
        )
        return {"FINISHED"}


class ImportDXFWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_dxf_with_custom_settings"
    bl_label = "Import AutoCAD DXF File"

    # properties
    merge: BoolProperty(default=True, name="Merged Objects")
    merge_options: EnumProperty(
        name="Merge Options",
        default="BY_LAYER",
        items=[
            ("BY_LAYER", "By Layer", ""),
            ("BY_TYPE", "By Layer AND DXF-Type", ""),
            ("BY_CLOSED_NO_BULGE_POLY", "By Layer AND closed no-bulge polys", ""),
            ("BY_BLOCKS", "By Layer AND DXF-Type AND Blocks", ""),
        ],
    )
    scene_options: EnumProperty(
        name="Scene",
        default="CURRENT_SCENE",
        items=[
            ("CURRENT_SCENE", "Current", ""),
            ("NEW_SCENE", "New", ""),
            ("NEW_UNIQUE_SCENE", "Unique", ""),
        ],
    )
    collection_options: EnumProperty(
        name="Collection",
        default="CURRENT_COLLECTION",
        items=[
            ("CURRENT_COLLECTION", "Current", ""),
            ("NEW_COLLECTION", "New", ""),
            ("SCENE_COLLECTION", "Scene", ""),
        ],
    )
    recenter: BoolProperty(default=False, name="Center geometry to scene")
    import_text: BoolProperty(default=True, name="Import Text")
    import_light: BoolProperty(default=True, name="Import Lights")

    # ui properties required by Natsuneko's base class logic
    import_section: BoolProperty(default=True, name="Import Options")
    merge_section: BoolProperty(default=True, name="Merge Options")
    optional_section: BoolProperty(default=True, name="Optional Objects")
    view_section: BoolProperty(default=True, name="View Options")

    def draw(self, context: Context):
        # Import Section
        column, state = self.get_expand_column("import_section")
        if state:
            column.prop(self, "scene_options")
            column.prop(self, "collection_options")

        # Merge Section
        column, state = self.get_expand_column("merge_section")
        if state:
            column.prop(self, "merge")
            sub = column.row()
            sub.enabled = self.merge
            sub.prop(self, "merge_options")

        # Optional Section
        column, state = self.get_expand_column("optional_section")
        if state:
            column.prop(self, "import_text")
            column.prop(self, "import_light")

        # View Section
        column, state = self.get_expand_column("view_section")
        if state:
            column.prop(self, "recenter")

    def execute(self, context: Context):
        # Ensure the built-in DXF extension is enabled
        if not hasattr(bpy.ops.import_scene, 'dxf'):
            try:
                bpy.ops.preferences.addon_enable(module="io_import_dxf")
            except Exception:
                pass
        
        filepath = self.filepath()
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)

        try:
            bpy.ops.import_scene.dxf(
                'EXEC_DEFAULT',
                filepath=filepath,
                directory=directory,
                files=[{'name': filename}],
                merge=self.merge,
                merge_options=self.merge_options,
                scene_options=self.scene_options,
                collection_options=self.collection_options,
                recenter=self.recenter,
                import_text=self.import_text,
                import_light=self.import_light,
            )
        except Exception as e:
            self.report({'ERROR'}, f"DXF Import Error: {e}")
            print(f"DXF Import Error: {e}")
            return {"CANCELLED"}

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_DXF(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import AutoCAD DXF File"

    @staticmethod
    def format():
        return "dxf"


class VIEW3D_FH_Import_DXF(bpy.types.FileHandler):
    bl_idname = "VIEW3D_FH_Import_DXF"
    bl_label = "Import AutoCAD DXF File"
    bl_import_operator = "object.drop_event_listener"
    bl_file_extensions = ".dxf"

    @classmethod
    def poll_drop(cls, context: bpy.types.Context | None) -> bool:
        if context is None:
            return False
        return context and context.area and context.area.type == "VIEW_3D"


OPERATORS: list[type] = [
    ImportDXFWithDefaults,
    ImportDXFWithCustomSettings,
    VIEW3D_MT_Space_Import_DXF,
    VIEW3D_FH_Import_DXF,
]