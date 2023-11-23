# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportUnboundVariable=false
# pyright: reportUnknownArgumentType=false

bl_info = {
    "name": "Drag and Drop Support",
    "author": "Natsuneko",
    "description": "Blender add-on for import some files from drag-and-drop",
    "blender": (3, 1, 0),
    "version": (3, 0, 0),
    "location": "Drag and Drop Support",
    "warning": "",
    "category": "Import-Export",
}


if "bpy" in locals():
    import importlib

    importlib.reload(formats)
    importlib.reload(menus)
    importlib.reload(operator)
else:
    from . import formats
    from . import menus
    from . import operator

import bpy  # nopep8
import ctypes  # nopep8

dll: ctypes.CDLL

classes: list[type] = [
    # menus
    menus.VIEW3D_MT_Space_Import_STL,
    menus.VIEW3D_MT_Space_Import_SVG,
    menus.VIEW3D_MT_Space_Import_USD,
    menus.VIEW3D_MT_Space_Import_USDA,
    menus.VIEW3D_MT_Space_Import_USDC,
    menus.VIEW3D_MT_Space_Import_X3D,
    menus.VIEW3D_MT_Space_Import_WRL,
    # operators
    operator.DropEventListener,  # type: ignore
]

classes.extend(formats.CLASSES)


def register():
    global classes
    global dll

    # register classes
    for c in classes:
        bpy.utils.register_class(c)

    # load injector dll
    import os

    dirname = os.path.dirname(__file__)
    injector = os.path.join(dirname, "blender-injection.dll")

    dll = ctypes.cdll.LoadLibrary(injector)


def unregister():
    global classes
    global dll

    # unregister classes
    for c in classes:
        bpy.utils.unregister_class(c)  # pyright: ignore[reportUnknownMemberType]

    # unload injector dll
    import _ctypes

    _ctypes.FreeLibrary(dll._handle)  # pyright: ignore[reportGeneralTypeIssues,reportUnknownMemberType]


if __name__ == "__main__":
    register()
