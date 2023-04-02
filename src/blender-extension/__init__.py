# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------


import ctypes

bl_info = {
    "name": "Drag and Drop Support",
    "author": "Natsuneko",
    "description": "Blender add-on for import some files from drag-and-drop",
    "blender": (3, 1, 0),
    "version": (2, 5, 0),
    "location": "Drag and Drop Support",
    "warning": "",
    "category": "Import-Export"
}


if "bpy" in locals():
    import importlib
    importlib.reload(operator)
    importlib.reload(properties)
    importlib.reload(ui)
else:
    from . import operator
    from . import properties
    from . import ui

    import bpy
    from bpy.props import PointerProperty

dll: ctypes.CDLL

classes = [
    operator.DropEventListener2,
    properties.DragAndDropSupportProperties,
    ui.DropEventListenerUI,
    ui.DropAlembicPropertiesUI,
    ui.DropBvhPropertiesUI,
    ui.DropFbxPropertiesUI,
    ui.DropColladaPropertiesUI,
    ui.DropGltfPropertiesUI,
    ui.DropObjPropertiesUI,
    ui.DropPlyPropertiesUI,
    ui.DropStlPropertiesUI,
    ui.DropUsdPropertiesUI,
    ui.DropX3dPropertiesUI,
]


def register():
    global classes
    global dll

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.DragAndDropSupportProperties = PointerProperty(
        type=properties.DragAndDropSupportProperties)

    import os

    dirname = os.path.dirname(__file__)
    injector = os.path.join(dirname, "blender-injection.dll")

    dll = ctypes.cdll.LoadLibrary(injector)


def unregister():
    global classes
    global dll

    for c in classes:
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.DragAndDropSupportProperties

    import _ctypes
    _ctypes.FreeLibrary(dll._handle)


if __name__ == "__main__":
    register()
