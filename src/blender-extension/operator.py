# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

from __future__ import annotations
from cmath import log
from enum import auto
from glob import glob
from typing import Callable, Dict

import bpy
import os

from bpy.types import Operator

from .properties import DragAndDropSupportProperties

import_dic: Dict[str, Callable[[str, DragAndDropSupportProperties], None]] = {
    ".abc": lambda w, props: bpy.ops.wm.alembic_import(filepath=w, scale=props.alembic_scale, set_frame_range=props.set_frame_range, validate_meshes=props.validate_meshes, is_sequence=props.is_sequence, as_background_job=props.as_background_job),
    ".bvh": lambda w, props: bpy.ops.import_anim.bvh(filepath=w, target=props.target, global_scale=props.bvh_global_scale, frame_start=props.frame_start, use_fps_scale=props.use_fps_scale, update_scene_fps=props.update_scene_fps, update_scene_duration=props.update_scene_duration, use_cyclic=props.use_cyclic, rotate_mode=props.rotate_mode, axis_forward=props.bvh_axis_forward, axis_up=props.bvh_axis_up),
    ".fbx": lambda w, props: bpy.ops.import_scene.fbx(filepath=w, ui_tab=props.ui_tab, use_manual_orientation=props.use_manual_orientation, global_scale=props.fbx_global_scale, bake_space_transform=props.bake_space_transform, use_custom_normals=props.use_custom_normals, use_image_search=props.fbx_use_image_search, use_alpha_decals=props.use_alpha_decals, decal_offset=props.decal_offset, use_anim=props.use_anim, anim_offset=props.anim_offset, use_subsurf=props.use_subsurf, use_custom_props=props.use_custom_props, use_custom_props_enum_as_string=props.use_custom_props_enum_as_string, ignore_leaf_bones=props.ignore_leaf_bones, force_connect_children=props.force_connect_children, automatic_bone_orientation=props.automatic_bone_orientation, primary_bone_axis=props.primary_bone_axis, secondary_bone_axis=props.secondary_bone_axis, use_prepost_rot=props.use_prepost_rot, axis_forward=props.fbx_axis_forward, axis_up=props.fbx_axis_up),
    ".dae": lambda w, props: bpy.ops.wm.collada_import(filepath=w, import_units=props.import_units, fix_orientation=props.fix_orientation, find_chains=props.find_chains, auto_connect=props.auto_connect, min_chain_length=props.min_chain_length, keep_bind_info=props.keep_bind_info),
    ".glb": lambda w, props: bpy.ops.import_scene.gltf(filepath=w, loglevel=props.loglevel, import_pack_images=props.import_pack_images, merge_vertices=props.merge_vertices, import_shading=props.import_shading, bone_heuristic=props.bone_heuristic, guess_original_bind_pose=props.guess_original_bind_pose),
    ".gltf": lambda w, props: bpy.ops.import_scene.gltf(filepath=w, loglevel=props.loglevel, import_pack_images=props.import_pack_images, merge_vertices=props.merge_vertices, import_shading=props.import_shading, bone_heuristic=props.bone_heuristic, guess_original_bind_pose=props.guess_original_bind_pose),
    ".obj": lambda w, props: bpy.ops.import_scene.obj(filepath=w, use_edges=props.use_edges, use_smooth_groups=props.use_smooth_groups, use_split_groups=props.use_split_groups, use_split_objects=props.use_split_objects, use_groups_as_vgroups=props.use_groups_as_vgroups, split_mode=props.split_mode, global_clamp_size=props.global_clamp_size, axis_forward=props.obj_axis_forward, axis_up=props.obj_axis_up),
    ".ply": lambda w, props: bpy.ops.import_mesh.ply(filepath=w, hide_props_region=props.hide_props_region),
    ".stl": lambda w, props: bpy.ops.import_mesh.stl(filepath=w, global_scale=props.stl_global_scale, use_scene_unit=props.use_scene_unit, use_facet_normal=props.use_facet_normal, axis_forward=props.stl_axis_forward, axis_up=props.stl_axis_up),
    ".svg": lambda w, props: bpy.ops.import_curve.svg(filepath=w),
    ".usd": lambda w, props: bpy.ops.wm.usd_import(filepath=w, scale=props.usd_scale, set_frame_range=props.usd_set_frame_range, import_cameras=props.import_cameras, import_curves=props.import_curves, import_lights=props.import_lights, import_materials=props.import_materials, import_meshes=props.import_meshes, import_volumes=props.import_volumes, import_subdiv=props.import_subdiv, import_instance_proxies=props.import_instance_proxies, import_visible_only=props.import_visible_only, create_collection=props.create_collection, read_mesh_uvs=props.read_mesh_uvs, read_mesh_colors=props.read_mesh_colors, import_guide=props.import_guide, import_proxy=props.import_proxy, import_render=props.import_render, import_usd_preview=props.import_usd_preview, set_material_blend=props.set_material_blend, light_intensity_scale=props.light_intensity_scale),
    ".usda": lambda w, props: bpy.ops.wm.usd_import(filepath=w, scale=props.usd_scale, set_frame_range=props.usd_set_frame_range, import_cameras=props.import_cameras, import_curves=props.import_curves, import_lights=props.import_lights, import_materials=props.import_materials, import_meshes=props.import_meshes, import_volumes=props.import_volumes, import_subdiv=props.import_subdiv, import_instance_proxies=props.import_instance_proxies, import_visible_only=props.import_visible_only, create_collection=props.create_collection, read_mesh_uvs=props.read_mesh_uvs, read_mesh_colors=props.read_mesh_colors, import_guide=props.import_guide, import_proxy=props.import_proxy, import_render=props.import_render, import_usd_preview=props.import_usd_preview, set_material_blend=props.set_material_blend, light_intensity_scale=props.light_intensity_scale),
    ".usdc": lambda w, props: bpy.ops.wm.usd_import(filepath=w, scale=props.usd_scale, set_frame_range=props.usd_set_frame_range, import_cameras=props.import_cameras, import_curves=props.import_curves, import_lights=props.import_lights, import_materials=props.import_materials, import_meshes=props.import_meshes, import_volumes=props.import_volumes, import_subdiv=props.import_subdiv, import_instance_proxies=props.import_instance_proxies, import_visible_only=props.import_visible_only, create_collection=props.create_collection, read_mesh_uvs=props.read_mesh_uvs, read_mesh_colors=props.read_mesh_colors, import_guide=props.import_guide, import_proxy=props.import_proxy, import_render=props.import_render, import_usd_preview=props.import_usd_preview, set_material_blend=props.set_material_blend, light_intensity_scale=props.light_intensity_scale),
    ".x3d": lambda w, props: bpy.ops.import_scene.x3d(filepath=w, axis_forward=props.x3d_axis_forward, axis_up=props.x3d_axis_up),
    ".wrl": lambda w, props: bpy.ops.import_scene.x3d(filepath=w, axis_forward=props.x3d_axis_forward, axis_up=props.x3d_axis_up),
}


class DropEventListener(Operator):
    bl_idname = "object.drop_event_listener"
    bl_label = "Drop Event Listener"

    __listening = False

    @classmethod
    def is_listening(cls):
        return cls.__listening

    @classmethod
    def reset(cls):
        cls.__listening = False

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

            props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

            importer(w=path, props=props)
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
