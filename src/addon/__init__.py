# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------


bl_info = {
    "name": "Drag and Drop Support",
    "author": "Natsuneko",
    "description": "Blender add-on for import some files from drag-and-drop",
    "blender": (3, 1, 0),
    "version": (2, 8, 0),
    "location": "Drag and Drop Support",
    "warning": "",
    "category": "Import-Export",
}


if "bpy" in locals():
    import importlib

    importlib.reload(menus)  # type: ignore
    importlib.reload(operator)  # type: ignore
else:
    from . import menus
    from . import operator
    from . import operators

import bpy  # nopep8
import ctypes  # nopep8

dll: ctypes.CDLL

classes = (
    # menus
    menus.VIEW3D_MT_Space_Import_ABC,  # type: ignore
    menus.VIEW3D_MT_Space_Import_BVH,  # type: ignore
    menus.VIEW3D_MT_Space_Import_DAE,  # type: ignore
    menus.VIEW3D_MT_Space_Import_FBX,  # type: ignore
    menus.VIEW3D_MT_Space_Import_GLB,  # type: ignore
    menus.VIEW3D_MT_Space_Import_GLTF,  # type: ignore
    menus.VIEW3D_MT_Space_Import_OBJ,  # type: ignore
    menus.VIEW3D_MT_Space_Import_PLY,  # type: ignore
    menus.VIEW3D_MT_Space_Import_STL,  # type: ignore
    menus.VIEW3D_MT_Space_Import_SVG,  # type: ignore
    menus.VIEW3D_MT_Space_Import_USD,  # type: ignore
    menus.VIEW3D_MT_Space_Import_USDA,  # type: ignore
    menus.VIEW3D_MT_Space_Import_USDC,  # type: ignore
    menus.VIEW3D_MT_Space_Import_VRM,  # type: ignore
    menus.VIEW3D_MT_Space_Import_X3D,  # type: ignore
    menus.VIEW3D_MT_Space_Import_WRL,  # type: ignore
    # operators
    operator.DropEventListener,  # type: ignore
    # operators (default importers)
    operator.ImportABCWithDefaults,  # type: ignore
    operator.ImportBVHWithDefaults,  # type: ignore
    operator.ImportDAEWithDefaults,  # type: ignore
    operator.ImportPLYWithDefaults,  # type: ignore
    operator.ImportSTLWithDefaults,  # type: ignore
    operator.ImportSVGWithDefaults,  # type: ignore
    operator.ImportUSDWithDefaults,  # type: ignore
    operator.ImportX3DWithDefaults,  # type: ignore
    # operators
    operators.fbx.ImportFBXWithDefaults,  # type: ignore
    operators.fbx.ImportFBXWithCustomSettings,  # type: ignore
    operators.glb.ImportGLBWithDefaults,  # type: ignore
    operators.glb.ImportGLBWithCustomSettings,  # type: ignore
    operators.obj.ImportOBJWithDefaults,  # type: ignore
    operators.obj.ImportOBJWithCustomSettings,  # type: ignore
    operators.obj_legacy.ImportOBJLegacyWithDefaults,  # type: ignore
    operators.obj_legacy.ImportOBJLegacyWithCustomSettings,  # type: ignore
    operators.vrm.ImportVRMWithDefaults,  # type: ignore
    operators.vrm.ImportVRMWithCustomSettings,  # type: ignore
)


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
        bpy.utils.unregister_class(c)  # type: ignore

    # unload injector dll
    import _ctypes

    _ctypes.FreeLibrary(dll._handle)  # type: ignore


if __name__ == "__main__":
    register()
