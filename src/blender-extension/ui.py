# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

from bpy.types import Panel

from .operator import DropEventListener
from .properties import DragAndDropSupportProperties


class DropEventListenerUI(Panel):
    bl_idname = "UI_PT_DropEventListener"
    bl_label = "Listener"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        cls = DropEventListener
        layout = self.layout

        if not cls.is_listening():
            layout.operator(cls.bl_idname, text="Start Listening", icon="PLAY")
        else:
            layout.operator(cls.bl_idname, text="Stop Listening", icon="PAUSE")


class DropAlembicPropertiesUI(Panel):
    bl_idname = "UI_PT_AlembicProperties"
    bl_label = "Alembic Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "alembic_scale")
        column.prop(props, "set_frame_range")
        column.prop(props, "validate_meshes")
        column.prop(props, "always_add_cache_render")
        column.prop(props, "is_sequence")
        column.prop(props, "as_background_job")


class DropBvhPropertiesUI(Panel):
    bl_idname = "UI_PT_MotionCaptureProperties"
    bl_label = "Motion Capture (BVH) Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "target")
        column.prop(props, "bvh_global_scale")
        column.prop(props, "frame_start")
        column.prop(props, "use_fps_scale")
        column.prop(props, "update_scene_fps")
        column.prop(props, "update_scene_duration")
        column.prop(props, "use_cyclic")
        column.prop(props, "rotate_mode")
        column.prop(props, "bvh_axis_forward")
        column.prop(props, "bvh_axis_up")


class DropFbxPropertiesUI(Panel):
    bl_idname = "UI_PT_FBXProperties"
    bl_label = "FBX Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "ui_tab")
        column.prop(props, "use_manual_orientation")
        column.prop(props, "fbx_global_scale")
        column.prop(props, "bake_space_transform")
        column.prop(props, "use_custom_normals")
        column.prop(props, "fbx_use_image_search")
        column.prop(props, "use_alpha_decals")
        column.prop(props, "decal_offset")
        column.prop(props, "use_anim")
        column.prop(props, "anim_offset")
        column.prop(props, "use_subsurf")
        column.prop(props, "use_custom_props")
        column.prop(props, "use_custom_props_enum_as_string")
        column.prop(props, "ignore_leaf_bones")
        column.prop(props, "force_connect_children")
        column.prop(props, "automatic_bone_orientation")
        column.prop(props, "primary_bone_axis")
        column.prop(props, "secondary_bone_axis")
        column.prop(props, "use_prepost_rot")
        column.prop(props, "fbx_axis_forward")
        column.prop(props, "fbx_axis_up")


class DropColladaPropertiesUI(Panel):
    bl_idname = "UI_PT_ColladaProperties"
    bl_label = "Collada Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "import_units")
        column.prop(props, "fix_orientation")
        column.prop(props, "find_chains")
        column.prop(props, "auto_connect")
        column.prop(props, "min_chain_length")
        column.prop(props, "keep_bind_info")


class DropGltfPropertiesUI(Panel):
    bl_idname = "UI_PT_GltfProperties"
    bl_label = "glTF Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "loglevel")
        column.prop(props, "import_pack_images")
        column.prop(props, "merge_vertices")
        column.prop(props, "import_shading")
        column.prop(props, "bone_heuristic")
        column.prop(props, "guess_original_bind_pose")


class DropObjPropertiesUI(Panel):
    bl_idname = "UI_PT_ObjProperties"
    bl_label = "OBJ Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "use_edges")
        column.prop(props, "use_smooth_groups")
        column.prop(props, "use_split_objects")
        column.prop(props, "use_split_groups")
        column.prop(props, "use_groups_as_vgroups")
        column.prop(props, "obj_use_image_search")
        column.prop(props, "split_mode")
        column.prop(props, "global_clamp_size")
        column.prop(props, "obj_axis_forward")
        column.prop(props, "obj_axis_up")


class DropPlyPropertiesUI(Panel):
    bl_idname = "UI_PT_PlyProperties"
    bl_label = "PLY Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "hide_props_region")


class DropStlPropertiesUI(Panel):
    bl_idname = "UI_PT_StlProperties"
    bl_label = "STL Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "stl_global_scale")
        column.prop(props, "use_scene_unit")
        column.prop(props, "use_facet_normal")
        column.prop(props, "stl_axis_forward")
        column.prop(props, "stl_axis_up")


class DropUsdPropertiesUI(Panel):
    bl_idname = "UI_PT_UsdProperties"
    bl_label = "USD Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "usd_scale")
        column.prop(props, "usd_set_frame_range")
        column.prop(props, "import_cameras")
        column.prop(props, "import_curves")
        column.prop(props, "import_lights")
        column.prop(props, "import_materials")
        column.prop(props, "import_meshes")
        column.prop(props, "import_volumes")
        column.prop(props, "import_subdiv")
        column.prop(props, "import_instance_proxies")
        column.prop(props, "import_visible_only")
        column.prop(props, "create_collection")
        column.prop(props, "read_mesh_uvs")
        column.prop(props, "read_mesh_colors")
        column.prop(props, "import_guide")
        column.prop(props, "import_proxy")
        column.prop(props, "import_render")
        column.prop(props, "import_usd_preview")
        column.prop(props, "set_material_blend")
        column.prop(props, "light_intensity_scale")


class DropX3dPropertiesUI(Panel):
    bl_idname = "UI_PT_X3dProperties"
    bl_label = "X3D Properties"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Drag and Drop Support"

    def draw(self, context):
        layout = self.layout

        props: DragAndDropSupportProperties = context.scene.DragAndDropSupportProperties

        column = layout.column()
        column.use_property_split = True
        column.prop(props, "x3d_axis_forward")
        column.prop(props, "x3d_axis_up")
