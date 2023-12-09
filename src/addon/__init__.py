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
    "warning": "This addon uses C++ DLL code. Please check the documentation for more details.",
    "doc_url": "https://docs.natsuneko.com/en-us/drag-and-drop-support/",
    "tracker_url": "https://github.com/mika-f/blender-drag-and-drop/issues",
    "category": "Import-Export",
}


if "bpy" in locals():
    import importlib

    importlib.reload(formats)
    importlib.reload(operator)
else:
    from . import formats
    from . import operator

import bpy  # nopep8
import ctypes  # nopep8

dll: ctypes.CDLL

classes: list[type] = [
    operator.DropEventListener,
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
