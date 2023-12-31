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
    "version": (2, 15, 0),
    "location": "Drag and Drop Support",
    "doc_url": "https://docs.natsuneko.com/en-us/drag-and-drop-support/",
    "tracker_url": "https://github.com/mika-f/blender-drag-and-drop/issues",
    "category": "Import-Export",
}


if "bpy" in locals():
    import importlib

    importlib.reload(formats)
    importlib.reload(interop)
    importlib.reload(operator)
    importlib.reload(preferences)
else:
    from . import formats
    from . import interop
    from . import operator
    from . import preferences

    import bpy  # nopep8


classes: list[type] = [operator.DropEventListener, preferences.DragAndDropPreferences]

classes.extend(formats.CLASSES)


def register():
    global classes

    # register classes
    for c in classes:
        bpy.utils.register_class(c)

    interop.try_load()


def unregister():
    global classes

    # unregister classes
    for c in classes:
        bpy.utils.unregister_class(c)  # pyright: ignore[reportUnknownMemberType]

    interop.try_unload()


if __name__ == "__main__":
    register()
