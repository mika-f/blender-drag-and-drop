# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

from __future__ import annotations

import bpy
import os
import typing

from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty  # type: ignore
from bpy.types import Context, Event, Operator

from .menus import VIEW3D_MT_Space_Import_BASE

# formats that Blender does not supported by default
conditionals: typing.Dict[str, typing.Callable[[], bool]] = {
    "vrm": lambda: hasattr(bpy.ops.import_scene, "vrm"),
}


class DropEventListener(Operator):
    bl_idname = "object.drop_event_listener"
    bl_label = "Open File via Drag and Drop"

    filename: StringProperty()  # type: ignore

    def inflate(self, name: str):
        VIEW3D_MT_Space_Import_BASE.filename = self.filename  # type: ignore
        bpy.ops.wm.call_menu(name=name)  # type: ignore
        return

    def invoke(self, context: Context, event: Event):
        try:
            path = typing.cast(str, self.filename)  # type: ignore
            _, ext = os.path.splitext(path)

            if ext[1:] in conditionals:
                if not conditionals[ext[1:].lower()]():
                    return {"FINISHED"}

            # dynamically called importer
            name = f"VIEW3D_MT_Space_Import_{ext[1:].upper()}"
            self.inflate(name)
        except TypeError as e:
            print(e)

        return {"FINISHED"}


class ImportWithDefaultsBase(Operator):
    filename: StringProperty()

    def filepath(self) -> str:
        return typing.cast(str, self.filename)


class ImportsWithCustomSettingsBase(ImportWithDefaultsBase):
    bl_options = {"REGISTER", "UNDO"}

    def get_expand_state(self, name: str) -> bool:
        return getattr(self, name)

    def get_expand_state_icon(self, name: str) -> str:
        return "TRIA_DOWN" if self.get_expand_state(name) else "TRIA_RIGHT"

    def get_expand_column(self, name: str) -> tuple[bpy.types.UILayout, bool]:
        box = self.layout.box()
        column = box.column()
        row = column.row(align=True)
        row.alignment = "LEFT"
        row.prop(self, name, icon=self.get_expand_state_icon(name), emboss=False)

        column.use_property_split = True

        return (column, self.get_expand_state(name))

    def invoke(self, context: Context, event: Event):
        wm = context.window_manager

        return wm.invoke_props_dialog(self)


class ImportABCWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_abc_with_defaults"
    bl_label = "Import Alembic File"

    def execute(self, context: Context):
        bpy.ops.wm.alembic_import(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportBVHWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_bvh_with_defaults"
    bl_label = "Import Biovision Hierarchy File"

    def execute(self, context: Context):
        bpy.ops.import_anim.bvh(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportDAEWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_dae_with_defaults"
    bl_label = "Import Collada File"

    def execute(self, context: Context):
        bpy.ops.wm.collada_import(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportFBXWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_fbx_with_defaults"
    bl_label = "Import FBX File"

    def execute(self, context: Context):
        bpy.ops.import_scene.fbx(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportFBXWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_fbx_with_custom_settings"
    bl_label = "Import FBX File"

    # Properties based on Blender latest (ordered by parameters on documents)
    use_manual_orientation: BoolProperty(default=False, name="Manual Orientation")
    global_scale: FloatProperty(default=1.0, name="Global Scale", min=0.001, max=1000)
    bake_space_transform: BoolProperty(default=False, name="Apply Transform")
    use_custom_normals: BoolProperty(default=True, name="Custom Normals")
    use_image_search: BoolProperty(default=True, name="Image Search")
    use_alpha_decals: BoolProperty(default=False, name="Alpha Decals")
    decal_offset: FloatProperty(default=0.0, name="Decal Offset", min=0, max=1)
    use_anim: BoolProperty(default=True, name="Animation")
    anim_offset: FloatProperty(default=1.0, name="Animation Offset")
    use_subsurf: BoolProperty(default=False, name="Subdivision Data")
    use_custom_props: BoolProperty(default=True, name="Custom Properties")
    use_custom_props_enum_as_string: BoolProperty(default=True, name="Import Enums As Strings")
    ignore_leaf_bones: BoolProperty(default=False, name="Ignore Leaf Bones")
    force_connect_children: BoolProperty(default=False, name="Force Connect Children")
    automatic_bone_orientation: BoolProperty(default=False, name="Automatic Bone Orientation")
    primary_bone_axis: EnumProperty(
        default="Y",
        name="Primary Bone Axis",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""), ("-X", "-X", ""), ("-Y", "-Y", ""), ("-Z", "-Z", "")],
    )
    secondary_bone_axis: EnumProperty(
        default="X",
        name="Secondary Bone Axis",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""), ("-X", "-X", ""), ("-Y", "-Y", ""), ("-Z", "-Z", "")],
    )
    use_prepost_rot: BoolProperty(default=True, name="Use Pre/Post Rotation")
    axis_forward: EnumProperty(
        default="-Z",
        name="Axis Forward",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""), ("-X", "-X", ""), ("-Y", "-Y", ""), ("-Z", "-Z", "")],
    )
    axis_up: EnumProperty(
        default="Y",
        name="Axis Up",
        items=[("X", "X", ""), ("Y", "Y", ""), ("Z", "Z", ""), ("-X", "-X", ""), ("-Y", "-Y", ""), ("-Z", "-Z", "")],
    )

    # added by Blender 3.4
    colors_type: EnumProperty(
        default="SRGB",
        name="Vertex Colors",
        items=[("NONE", "None", ""), ("SRGB", "sRGB", ""), ("LINEAR", "Linear", "")],
    )

    # ui properties
    include_section: BoolProperty(default=True, name="Include")
    transform_section: BoolProperty(default=True, name="Transform")
    animation_section: BoolProperty(default=True, name="Animation")
    armature_section: BoolProperty(default=True, name="Armature")

    def draw(self, context: Context):
        # Include Section
        column, state = self.get_expand_column("include_section")

        if state:
            column.prop(self, "use_custom_normals")
            column.prop(self, "use_subsurf")
            column.prop(self, "use_custom_props")
            column.prop(self, "use_custom_props_enum_as_string")
            column.prop(self, "use_image_search")

            if bpy.app.version >= (3, 4, 0):
                column.prop(self, "colors_type")

        # Transform Section
        column, state = self.get_expand_column("transform_section")

        if state:
            column.prop(self, "global_scale")
            column.prop(self, "decal_offset")

            row = column.row()
            row.prop(self, "bake_space_transform")
            row.label(text="", icon="ERROR")

            column.prop(self, "use_prepost_rot")
            column.prop(self, "use_manual_orientation")

            orientation = column.column()
            orientation.enabled = self.use_manual_orientation
            orientation.prop(self, "axis_forward")
            orientation.prop(self, "axis_up")

        # Animation Section
        column, state = self.get_expand_column("animation_section")

        if state:
            column.prop(self, "use_anim")

            animation = column.column()
            animation.enabled = self.use_anim
            animation.prop(self, "anim_offset")

        # Armature Section
        column, state = self.get_expand_column("armature_section")

        if state:
            column.prop(self, "ignore_leaf_bones")
            column.prop(self, "force_connect_children")
            column.prop(self, "automatic_bone_orientation")
            column.prop(self, "primary_bone_axis")
            column.prop(self, "secondary_bone_axis")

    def execute(self, context: Context):
        bpy.ops.import_scene.fbx(
            filepath=self.filepath(),
            use_manual_orientation=self.use_manual_orientation,
            global_scale=self.global_scale,
            bake_space_transform=self.bake_space_transform,
            use_custom_normals=self.use_custom_normals,
            colors_type=self.colors_type,
            use_image_search=self.use_image_search,
            use_alpha_decals=self.use_alpha_decals,
            decal_offset=self.decal_offset,
            use_anim=self.use_anim,
            anim_offset=self.anim_offset,
            use_subsurf=self.use_subsurf,
            use_custom_props=self.use_custom_props,
            use_custom_props_enum_as_string=self.use_custom_props_enum_as_string,
            ignore_leaf_bones=self.ignore_leaf_bones,
            force_connect_children=self.force_connect_children,
            automatic_bone_orientation=self.automatic_bone_orientation,
            primary_bone_axis=self.primary_bone_axis,
            secondary_bone_axis=self.secondary_bone_axis,
            use_prepost_rot=self.use_prepost_rot,
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
        )

        return {"FINISHED"}


class ImportGLBWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_glb_with_defaults"
    bl_label = "Import GLB File"

    def execute(self, context: Context):
        bpy.ops.import_scene.gltf(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportOBJWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_obj_with_defaults"
    bl_label = "Import Wavefront OBJ File"

    def execute(self, context: Context):
        bpy.ops.wm.obj_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportOBJLegacyWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_obj_legacy_with_defaults"
    bl_label = "Import Wavefront OBJ File"

    def execute(self, context: Context):
        bpy.ops.import_scene.obj(filepath=self.filepath())
        return {"FINISHED"}


class ImportOBJWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_obj_with_custom_settings"
    bl_label = "Import Wavefront OBJ File"

    # properties
    global_scale: FloatProperty(default=1.0, name="Scale", min=0.0001, max=10000)
    clamp_size: FloatProperty(default=0.0, name="Clamp Bounding Box", min=0, max=1000)
    forward_axis: EnumProperty(
        name="Forward Axis",
        default="-Z",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )
    up_axis: EnumProperty(
        name="Up Axis",
        default="Y",
        items=[
            ("X", "X", ""),
            ("Y", "Y", ""),
            ("Z", "Z", ""),
            ("-X", "-X", ""),
            ("-Y", "-Y", ""),
            ("-Z", "-Z", ""),
        ],
    )
    use_split_objects: BoolProperty(default=True, name="Split by Object")
    use_split_groups: BoolProperty(default=False, name="Split by Group")
    import_vertex_groups: BoolProperty(default=False, name="Vertex Groups")
    validate_meshes: BoolProperty(default=False, name="Validate Meshes")

    # ui properties
    transform_section: BoolProperty(default=True, name="Transform")
    options_section: BoolProperty(default=True, name="Options")

    def draw(self, context: Context):
        # Transform Section
        column, state = self.get_expand_column("transform_section")

        if state:
            column.prop(self, "global_scale")
            column.prop(self, "clamp_size")
            column.prop(self, "forward_axis")
            column.prop(self, "up_axis")

        # Options Section
        column, state = self.get_expand_column("options_section")

        if state:
            column.prop(self, "use_split_objects")
            column.prop(self, "use_split_groups")
            column.prop(self, "import_vertex_groups")
            column.prop(self, "validate_meshes")

    def execute(self, context: Context):
        bpy.ops.wm.obj_import(
            filepath=self.filepath(),
            global_scale=self.global_scale,
            clamp_size=self.clamp_size,
            forward_axis=self.forward_axis,
            up_axis=self.up_axis,
            use_split_objects=self.use_split_objects,
            use_split_groups=self.use_split_groups,
            import_vertex_groups=self.import_vertex_groups,
            validate_meshes=self.validate_meshes,
        )

        return {"FINISHED"}


class ImportOBJLegacyWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_obj_legacy_with_custom_settings"
    bl_label = "Import Wavefront OBJ File"

    # deprecated properties (>= 3.4.0)
    use_edges: BoolProperty(default=True, name="Lines")
    use_smooth_groups: BoolProperty(default=True, name="Smooth Groups")
    use_split_objects: BoolProperty(default=True, name="Split by Object")
    use_split_groups: BoolProperty(default=False, name="Split by Group")
    use_groups_as_vgroups: BoolProperty(default=False, name="Poly Groups")
    use_image_search: BoolProperty(default=True, name="Image Search")
    split_mode: EnumProperty(
        default="ON",
        name="Split",
        items=[
            ("ON", "Split", ""),
            ("OFF", "Keep Vert Order", ""),
        ],
    )
    global_clamp_size: FloatProperty(default=0.0, name="Clamp Size", min=0.0, max=1000.0)
    axis_forward: EnumProperty(
        default="-Z",
        name="Forward",
        items=[
            ("X", "X Forward", ""),
            ("Y", "Y Forward", ""),
            ("Z", "Z Forward", ""),
            ("-X", "-X Forward", ""),
            ("-Y", "-Y Forward", ""),
            ("-Z", "-Z Forward", ""),
        ],
    )
    axis_up: EnumProperty(
        default="Y",
        name="Up",
        items=[
            ("X", "X Up", ""),
            ("Y", "Y Up", ""),
            ("Z", "Z Up", ""),
            ("-X", "-X Up", ""),
            ("-Y", "-Y Up", ""),
            ("-Z", "-Z Up", ""),
        ],
    )

    # ui properties
    include_section: BoolProperty(default=True, name="Include")
    transform_section: BoolProperty(default=True, name="Transform")
    geometry_section: BoolProperty(default=True, name="Geometry")

    def draw(self, context: Context):
        # Include Section
        column, state = self.get_expand_column("include_section")

        if state:
            column.prop(self, "use_image_search")
            column.prop(self, "use_smooth_groups")
            column.prop(self, "use_edges")

        # Transform Section
        column, state = self.get_expand_column("transform_section")

        if state:
            column.prop(self, "global_clamp_size")
            column.prop(self, "axis_forward")
            column.prop(self, "axis_up")

        # Geometry Section
        column, state = self.get_expand_column("geometry_section")

        if state:
            row = column.row()
            row.prop(self, "split_mode", expand=True)

            if self.split_mode == "ON":
                column.prop(self, "use_split_objects")
                column.prop(self, "use_split_groups")
            else:
                column.prop(self, "use_groups_as_vgroups")

    def execute(self, context: Context):
        bpy.ops.import_scene.obj(
            filepath=self.filepath(),
            use_edges=self.use_edges,
            use_smooth_groups=self.use_smooth_groups,
            use_split_objects=self.use_split_objects,
            use_split_groups=self.use_split_groups,
            use_groups_as_vgroups=self.use_groups_as_vgroups,
            use_image_search=self.use_image_search,
            split_mode=self.split_mode,
            global_clamp_size=self.global_clamp_size,
            axis_forward=self.axis_forward,
            axis_up=self.axis_up,
        )

        return {"FINISHED"}


class ImportPLYWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_ply_with_defaults"
    bl_label = "Import PLY File"

    def execute(self, context: Context):
        bpy.ops.import_mesh.ply(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportSTLWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_stl_with_defaults"
    bl_label = "Import STL File"

    def execute(self, context: Context):
        bpy.ops.import_mesh.stl(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportSVGWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_svg_with_defaults"
    bl_label = "Import SVG File"

    def execute(self, context: Context):
        bpy.ops.import_curve.svg(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportUSDWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_svg_with_defaults"
    bl_label = "Import SVG File"

    def execute(self, context: Context):
        bpy.ops.wm.usd_import(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportVRMWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_vrm_with_defaults"
    bl_label = "Import VRM File"

    def execute(self, context: Context):
        bpy.ops.import_scene.vrm(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}


class ImportVRMWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_vrm_with_custom_settings"
    bl_label = "Import VRM File with Custom Settings"

    # properties
    # ref: https://github.com/saturday06/VRM-Addon-for-Blender/blob/d15fc0070835e9b9ec7622817691a89d52fceab7/io_scene_vrm/importer/import_scene.py#L73-L100
    extract_textures_into_folder: BoolProperty(default=False, name="Extract texture images into the folder")
    make_new_texture_folder: BoolProperty(default=True, name="Don't overwrite existing texture folder (limit:100,000)")
    set_shading_type_to_material_on_import: BoolProperty(default=True, name='Set shading type to "Material"')
    set_view_transform_to_standard_on_import: BoolProperty(default=True, name='Set view transform to "Standard"')
    set_armature_display_to_wire: BoolProperty(default=True, name='Set an imported armature display to "Wire"')
    set_armature_display_to_show_in_front: BoolProperty(
        default=True, name='Set an imported armature display to show "In-Front"'
    )

    def draw(self, context: Context):
        box = self.layout.box()
        column = box.column()

        column.use_property_split = True

        column.prop(self, "extract_textures_into_folder")
        column.prop(self, "make_new_texture_folder")
        column.prop(self, "set_shading_type_to_material_on_import")
        column.prop(self, "set_view_transform_to_standard_on_import")
        column.prop(self, "set_armature_display_to_wire")
        column.prop(self, "set_armature_display_to_show_in_front")

    def execute(self, context: Context):
        bpy.ops.import_scene.vrm(
            filepath=self.filepath(),
            extract_textures_into_folder=self.extract_textures_into_folder,
            make_new_texture_folder=self.make_new_texture_folder,
            set_shading_type_to_material_on_import=self.set_shading_type_to_material_on_import,
            set_view_transform_to_standard_on_import=self.set_view_transform_to_standard_on_import,
            set_armature_display_to_wire=self.set_armature_display_to_wire,
            set_armature_display_to_show_in_front=self.set_armature_display_to_show_in_front,
        )

        return {"FINISHED"}


class ImportX3DWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_x3d_with_defaults"
    bl_label = "Import X3D File"

    def execute(self, context: Context):
        bpy.ops.import_scene.x3d(filepath=self.filepath())  # type: ignore
        return {"FINISHED"}
