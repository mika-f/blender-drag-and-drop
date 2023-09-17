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

    def invoke(self, context: Context, event: Event):
        wm = context.window_manager

        return wm.invoke_props_dialog(self)
