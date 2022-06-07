# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

from __future__ import annotations

import bpy
import os

from bpy.types import Operator


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

            if ext == ".fbx":
                bpy.ops.import_scene.fbx(filepath=path)
            elif ext == ".gltf":
                bpy.ops.import_scene.gltf(filepath=path)
            elif ext == ".glb":
                bpy.ops.import_scene.gltf(filepath=path)
            elif ext == ".obj":
                bpy.ops.import_scene.obj(filepath=path)
            elif ext == ".x3d":
                bpy.ops.import_scene.x3d(filepath=path)
            else:
                print("unknown file")
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
