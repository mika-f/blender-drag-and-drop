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
    importlib.reload(properties)
    importlib.reload(ui)
else:
    from . import operator
    from . import properties
    from . import ui

    import bpy
    from bpy.props import PointerProperty
    from bpy.app.handlers import persistent


classes = [
    operator.DropEventListener,
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


@persistent
def post_handler(_):
    cls = operator.DropEventListener
    cls.reset()


def register():
    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.DragAndDropSupportProperties = PointerProperty(
        type=properties.DragAndDropSupportProperties)

    bpy.app.handlers.load_post.append(post_handler)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    del bpy.types.Scene.DragAndDropSupportProperties

    bpy.app.handlers.load_post.remove(post_handler)


if __name__ == "__main__":
    register()
