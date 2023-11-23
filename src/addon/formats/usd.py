# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

import bpy

from bpy.props import (
    BoolProperty,  # pyright: ignore[reportUnknownVariableType]
    EnumProperty,  # pyright: ignore[reportUnknownVariableType]
    FloatProperty,  # pyright: ignore[reportUnknownVariableType]
    StringProperty,  # pyright: ignore[reportUnknownVariableType]
)
from bpy.types import Context

from .super import (
    ImportWithDefaultsBase,
    ImportsWithCustomSettingsBase,
    VIEW3D_MT_Space_Import_BASE,
)


class ImportUSDWithDefaults(ImportWithDefaultsBase):
    bl_idname = "object.import_usd_with_defaults"
    bl_label = "Import Wavefront USD File (Experimental)"

    def execute(self, context: Context):
        bpy.ops.wm.usd_import(filepath=self.filepath())
        return {"FINISHED"}


class ImportUSDWithCustomSettings(ImportsWithCustomSettingsBase):
    bl_idname = "object.import_usd_with_custom_settings"
    bl_label = "Import Wavefront USD File (Experimental)"

    relative_path: BoolProperty(default=True, name="Relative Path")
    scale: FloatProperty(default=1.0, min=0.0001, max=1000, name="Scale")
    set_frame_range: BoolProperty(default=True, name="Set Frame Range")
    import_cameras: BoolProperty(default=True, name="Cameras")
    import_curves: BoolProperty(default=True, name="Curves")
    import_lights: BoolProperty(default=True, name="Lights")
    import_materials: BoolProperty(default=True, name="Materials")
    import_meshes: BoolProperty(default=True, name="Meshes")
    import_volumes: BoolProperty(default=True, name="Volumes")
    import_shapes: BoolProperty(default=True, name="Shapes")
    import_skeletons: BoolProperty(default=True, name="Skeletons")
    import_blendshapes: BoolProperty(default=True, name="Blend Shapes")
    import_subdiv: BoolProperty(default=False, name="Subdivision")
    import_instance_proxies: BoolProperty(default=True, name="Import Instance Proxies")
    import_visible_only: BoolProperty(default=True, name="Visible Primitives Only")
    create_collection: BoolProperty(default=False, name="Create Collection")
    read_mesh_uvs: BoolProperty(default=True, name="UV Coordinates")
    read_mesh_colors: BoolProperty(default=True, name="Color Attributes")
    read_mesh_attributes: BoolProperty(default=True, name="Mesh Attributes")
    prim_path_mask: StringProperty(default="", name="Path Mask")
    import_guide: BoolProperty(default=False, name="Guide")
    import_proxy: BoolProperty(default=True, name="Proxy")
    import_render: BoolProperty(default=True, name="Render")
    import_all_materials: BoolProperty(default=False, name="Import All Materials")
    import_usd_preview: BoolProperty(default=True, name="Import USD Preview")
    set_material_blend: BoolProperty(default=True, name="Set Material Blend")
    light_intensity_scale: FloatProperty(
        default=1.0, min=0.0001, max=10000, name="Light Intensity Scale"
    )
    mtl_name_collision_mode: EnumProperty(
        default="MAKE_UNIQUE",
        name="Material Name Collision",
        items=[
            ("MAKE_UNIQUE", "Make Unique", ""),
            ("REFERENCE_EXISTING", "Reference Existing", ""),
        ],
    )
    import_textures_mode: EnumProperty(
        default="IMPORT_PACK",
        name="Import Textures",
        items=[
            ("IMPORT_NONE", "None", ""),
            ("IMPORT_PACK", "Packed", ""),
            ("IMPORT_COPY", "Copy", ""),
        ],
    )
    import_textures_dir: StringProperty(
        default="//textures/", name="Textures Directory"
    )
    tex_name_collision_mode: EnumProperty(
        default="USE_EXISTING",
        name="File Name Collision",
        items=[("USE_EXISTING", "Use Existing", ""), ("OVERWRITE", "Overwrite", "")],
    )

    def draw(self, context: Context):
        column, box = self.get_heading_column("Data Types")
        column.prop(self, "import_cameras")
        column.prop(self, "import_curves")
        column.prop(self, "import_lights")
        column.prop(self, "import_materials")
        column.prop(self, "import_meshes")
        column.prop(self, "import_volumes")
        column.prop(self, "import_shapes")
        column.prop(self, "import_skeletons")
        column.prop(self, "import_blendshapes")

        column = self.get_column(box=box)
        column.prop(self, "prim_path_mask")
        column.prop(self, "scale")

        column, box = self.get_heading_column("Mesh Data")
        column.prop(self, "read_mesh_uvs")
        column.prop(self, "read_mesh_colors")
        column.prop(self, "read_mesh_attributes")

        column, _ = self.get_heading_column("Include", box=box)
        column.prop(self, "import_subdiv")
        column.prop(self, "import_instance_proxies")
        column.prop(self, "import_visible_only")
        column.prop(self, "import_guide")
        column.prop(self, "import_proxy")
        column.prop(self, "import_render")

        column, _ = self.get_heading_column("Options", box=box)
        column.prop(self, "set_frame_range")
        column.prop(self, "relative_path")
        column.prop(self, "create_collection")

        column = self.get_column(box=box)
        column.prop(self, "light_intensity_scale")

        column, box = self.get_heading_column("Materials")
        column.prop(self, "import_all_materials")
        column.prop(self, "import_usd_preview")

        usd_preview = column.column()
        usd_preview.enabled = self.import_usd_preview
        usd_preview.prop(self, "set_material_blend")

        column = self.get_column(box=box)
        column.prop(self, "mtl_name_collision_mode")

        column = self.get_column()
        column.prop(self, "import_textures_mode")

        texture_mode_copy = column.column()
        texture_mode_copy.enabled = self.import_textures_mode == "IMPORT_COPY"
        texture_mode_copy.prop(self, "import_textures_dir")
        texture_mode_copy.prop(self, "tex_name_collision_mode")

    def execute(self, context: Context):
        bpy.ops.wm.usd_import(
            filepath=self.filepath(),
            relative_path=self.relative_path,
            scale=self.scale,
            set_frame_range=self.set_frame_range,
            import_cameras=self.import_cameras,
            import_curves=self.import_curves,
            import_lights=self.import_lights,
            import_materials=self.import_materials,
            import_meshes=self.import_meshes,
            import_volumes=self.import_volumes,
            import_shapes=self.import_shapes,
            import_skeletons=self.import_skeletons,
            import_blendshapes=self.import_blendshapes,
            import_subdiv=self.import_subdiv,
            import_instance_proxies=self.import_instance_proxies,
            import_visible_only=self.import_visible_only,
            create_collection=self.create_collection,
            read_mesh_uvs=self.read_mesh_uvs,
            read_mesh_colors=self.read_mesh_colors,
            read_mesh_attributes=self.read_mesh_attributes,
            prim_path_mask=self.prim_path_mask,
            import_guide=self.import_guide,
            import_proxy=self.import_proxy,
            import_render=self.import_render,
            import_all_materials=self.import_all_materials,
            import_usd_preview=self.import_usd_preview,
            set_material_blend=self.set_material_blend,
            light_intensity_scale=self.light_intensity_scale,
            mtl_name_collision_mode=self.mtl_name_collision_mode,
            import_textures_mode=self.import_textures_mode,
            import_textures_dir=self.import_textures_dir,
            tex_name_collision_mode=self.tex_name_collision_mode,
        )

        return {"FINISHED"}


class VIEW3D_MT_Space_Import_USD(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    def format(self):
        return "usd"


class VIEW3D_MT_Space_Import_USDA(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    def format(self):
        return "usd"


class VIEW3D_MT_Space_Import_USDC(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    def format(self):
        return "usd"


class VIEW3D_MT_Space_Import_USDZ(VIEW3D_MT_Space_Import_BASE):
    bl_label = "Import Universal Scene Description File"

    def format(self):
        return "usd"


OPERATORS = [
    ImportUSDWithDefaults,
    ImportUSDWithCustomSettings,
    VIEW3D_MT_Space_Import_USD,
    VIEW3D_MT_Space_Import_USDA,
    VIEW3D_MT_Space_Import_USDC,
    VIEW3D_MT_Space_Import_USDZ,
]
