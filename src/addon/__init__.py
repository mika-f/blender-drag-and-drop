# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the GPLv3 License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportUnboundVariable=false
# pyright: reportUnknownArgumentType=false


if "bpy" in locals():
    import importlib

    importlib.reload(formats)
    importlib.reload(operator)
else:
    from . import formats
    from . import operator

    import bpy  # nopep8


classes: list[type] = []
classes.extend(operator.get_operators())
classes.extend(formats.CLASSES)


def has_native_file_handler(file_extensions: str) -> tuple[bool, str | None]:
    """
    Check if a third-party addon FileHandler exists for the given file extension(s).
    
    This only detects FileHandlers from OTHER addons, not Blender's built-in handlers.
    Respects other add-ons that add their own FileHandlers to avoid conflicts.
    
    Args:
        file_extensions: File extension(s) to check (e.g., ".3mf" or ".gltf;.glb")
    
    Returns:
        A tuple of (exists: bool, handler_name: str | None) indicating whether
        a third-party addon handler exists and its name if found.
    """
    if not hasattr(bpy, 'types'):
        return False, None
    
    # Normalize extensions to a set for comparison
    target_extensions = set(ext.strip().lower() for ext in file_extensions.split(';'))
    
    # Known Blender built-in FileHandler prefixes (these should NOT trigger skipping)
    builtin_prefixes = ('IO_FH_', 'IMPORT_SCENE_FH_', 'EXPORT_SCENE_FH_')
    
    # Iterate through all registered types to find FileHandler instances
    for attr_name in dir(bpy.types):
        try:
            attr = getattr(bpy.types, attr_name)
            
            # Check if this is a FileHandler class
            if (hasattr(attr, '__mro__') and 
                bpy.types.FileHandler in attr.__mro__ and
                attr != bpy.types.FileHandler):
                
                # Check if it has bl_file_extensions
                if hasattr(attr, 'bl_file_extensions'):
                    handler_extensions = attr.bl_file_extensions
                    
                    # Normalize handler extensions for comparison
                    handler_ext_set = set(ext.strip().lower() for ext in handler_extensions.split(';'))
                    
                    # Check if there's any overlap with target extensions
                    if target_extensions & handler_ext_set:
                        # Skip if it's this addon's own handler
                        if attr_name.startswith('VIEW3D_FH_Import_'):
                            continue
                        
                        # Skip if it's a Blender built-in handler
                        if attr_name.startswith(builtin_prefixes):
                            continue
                        
                        # Found a third-party addon handler!
                        return True, attr_name
        except (AttributeError, TypeError):
            # Skip attributes that can't be inspected
            continue
    
    return False, None


def register():
    global classes

    # Filter out FileHandler classes if addon-native handlers already exist
    classes_to_register = []
    
    for c in classes:
        # Check if this is a FileHandler class
        if (hasattr(c, '__mro__') and 
            hasattr(bpy.types, 'FileHandler') and
            bpy.types.FileHandler in c.__mro__):
            
            # Check if it has bl_file_extensions attribute
            if hasattr(c, 'bl_file_extensions'):
                file_extensions = c.bl_file_extensions
                has_native, native_handler_name = has_native_file_handler(file_extensions)
                
                if has_native:
                    print(
                        f"[Drag and Drop] Skipping registration of {c.__name__} for {file_extensions} - "
                        f"addon FileHandler '{native_handler_name}' already exists"
                    )
                    continue
        
        classes_to_register.append(c)
    
    # Register the filtered classes
    for c in classes_to_register:
        bpy.utils.register_class(c)


def unregister():
    global classes

    # unregister classes
    for c in classes:
        try:
            bpy.utils.unregister_class(c)  # pyright: ignore[reportUnknownMemberType]
        except:
            pass


if __name__ == "__main__":
    register()
