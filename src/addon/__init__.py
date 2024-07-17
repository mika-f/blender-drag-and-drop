# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
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


def register():
    global classes

    # register classes
    for c in classes:
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
