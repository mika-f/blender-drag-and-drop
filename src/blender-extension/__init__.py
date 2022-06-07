# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------


bl_info = {
    "name": "Drag and Drop Support",
    "author": "Natsuneko",
    "description": "Blender add-on for import some files from drag-and-drop",
    "blender": (3, 1, 0),
    "version": (0, 0, 1),
    "location": "Drag and Drop Support",
    "warning": "",
    "category": "Import-Export"
}

if "bpy" in locals():
    import importlib
    importlib.reload(operator)
    importlib.reload(ui)
else:
    from . import operator
    from . import ui

    import bpy


classes = [
    operator.DropEventListener,
    ui.DropEventListenerUI
]


def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
