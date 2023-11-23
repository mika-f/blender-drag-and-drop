# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

import bpy
import typing

from bpy.props import StringProperty  # type: ignore
from bpy.types import Context, Event, Operator


selectable_importers: typing.Dict[
    str, typing.Callable[[], typing.List[tuple[str, str]]]
] = {
    "obj": lambda: [("", "obj"), ("(Legacy)", "obj_legacy")] if bpy.app.version >= (3, 4, 0) else [("", "obj_legacy")],  # type: ignore
    "stl": lambda: [("", "stl"), ("(Legacy)", "stl_legacy")] if bpy.app.version >= (3, 4, 0) else [("", "stl_legacy")],  # type: ignore
}


class ImportWithDefaultsBase(Operator):
    filename: StringProperty()

    def filepath(self) -> str:
        return typing.cast(str, self.filename)


class ImportsWithCustomSettingsBase(ImportWithDefaultsBase):
    bl_options = {"REGISTER", "UNDO"}

    def get_expand_state(self, name: str) -> bool:
        return getattr(self, name)

    def get_expand_state_icon(self, name: str) -> str:
        return "TRIA_DOWN" if self.get_expand_state(name) else "TRIA_RIGHT"

    def get_expand_column(self, name: str) -> tuple[bpy.types.UILayout, bool]:
        box = self.layout.box()
        column = box.column()
        row = column.row(align=True)
        row.alignment = "LEFT"
        row.prop(self, name, icon=self.get_expand_state_icon(name), emboss=False)

        column.use_property_split = True

        return (column, self.get_expand_state(name))

    def get_column(self, box: bpy.types.UILayout | None = None) -> bpy.types.UILayout:
        box = self.layout.box() if box is None else box
        column = box.column()

        column.use_property_split = True

        return column

    def get_heading_column(
        self, heading: str, box: bpy.types.UILayout | None = None
    ) -> tuple[bpy.types.UILayout, bpy.types.UILayout]:
        box = self.layout.box() if box is None else box
        column = box.column(heading=heading)

        column.use_property_split = True

        return column, box

    def invoke(self, context: Context, event: Event):
        wm = context.window_manager

        return wm.invoke_props_dialog(self)


class VIEW3D_MT_Space_Import_BASE(bpy.types.Menu):
    filename: str

    def draw(self, context: Context | None):
        layout = self.layout
        format = self.format()

        if format in selectable_importers:
            importers = selectable_importers[format]()

            col = layout.column()

            for importer in importers:
                text, name = importer

                col.operator(
                    f"object.import_{name}_with_defaults",
                    text=f"Import with Defaults {text}".strip(),
                ).filename = VIEW3D_MT_Space_Import_BASE.filename  # type: ignore

            col = layout.column()
            col.operator_context = "INVOKE_DEFAULT"

            for importer in importers:
                text, name = importer

                col.operator(
                    f"object.import_{name}_with_custom_settings",
                    text=f"Import with Custom Settings {text}".strip(),
                ).filename = VIEW3D_MT_Space_Import_BASE.filename  # type: ignore

        else:
            col = layout.column()
            col.operator(
                f"object.import_{self.format()}_with_defaults",
                text="Import with Defaults",
            ).filename = VIEW3D_MT_Space_Import_BASE.filename  # type: ignore

            col = layout.column()
            col.operator_context = "INVOKE_DEFAULT"
            col.operator(
                f"object.import_{self.format()}_with_custom_settings",
                text="Import with Custom Settings",
            ).filename = VIEW3D_MT_Space_Import_BASE.filename  # type: ignore

    def format(self) -> str:
        return ""
