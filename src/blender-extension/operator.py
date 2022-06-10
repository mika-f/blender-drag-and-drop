# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

from __future__ import annotations
from typing import Callable, Dict

import bpy
import os

from bpy.types import Operator

import_dic: Dict[str, Callable[[str], None]] = {
    ".abc": lambda w: bpy.ops.wm.alembic_import(filepath=w),
    ".bvh": lambda w: bpy.ops.import_anim.bvh(filepath=w),
    ".fbx": lambda w: bpy.ops.import_scene.fbx(filepath=w),
    ".dae": lambda w: bpy.ops.wm.collada_import(filepath=w),
    ".glb": lambda w: bpy.ops.import_scene.gltf(filepath=w),
    ".gltf": lambda w: bpy.ops.import_scene.gltf(filepath=w),
    ".obj": lambda w: bpy.ops.import_scene.obj(filepath=w),
    ".ply": lambda w: bpy.ops.import_mesh.ply(filepath=w),
    ".stl": lambda w: bpy.ops.import_mesh.stl(filepath=w),
    ".svg": lambda w: bpy.ops.import_curve.svg(filepath=w),
    ".usd": lambda w: bpy.ops.wm.usd_import(filepath=w),
    ".usda": lambda w: bpy.ops.wm.usd_import(filepath=w),
    ".usdc": lambda w: bpy.ops.wm.usd_import(filepath=w),
    ".x3d": lambda w: bpy.ops.import_scene.x3d(filepath=w),
    ".wrl": lambda w: bpy.ops.import_scene.x3d(filepath=w),
}


class DropEventListener(Operator):
    bl_idname = "object.drop_event_listener"
    bl_label = "Drop Event Listener"

    __listening = False

    @classmethod
    def is_listening(cls):
        return cls.__listening

    def modal(self, context, event):
        if context.area:
            context.area.tag_redraw()

        if not self.is_listening():
            return {'FINISHED'}

        if bpy.types.Scene.ImportReq == 0:
            return {'PASS_THROUGH'}
        if bpy.types.Scene.ImportReq is None:
            return {'PASS_THROUGH'}

        try:
            path = bpy.types.Scene.ImportReq
            _, ext = os.path.splitext(path)

            importer = import_dic.get(ext, lambda w: print("unknown file"))
            importer(w=path)
        except TypeError as e:
            print(e)

        bpy.types.Scene.ImportReq = None

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        cls = DropEventListener

        if context.area.type == "VIEW_3D":
            bpy.types.Scene.ImportReq = None

            if not self.is_listening():
                cls.__listening = True
                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}

            else:
                cls.__listening = False

                return {'FINISHED'}
        else:
            return {'CANCELED'}
