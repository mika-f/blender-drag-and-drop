# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportGeneralTypeIssues=false
# pyright: reportUnknownArgumentType=false
# pyright: reportUnknownMemberType=false

import bpy
import ctypes
import os
import typing

is_load_native_library: bool = False
native_handler: ctypes.CDLL


def log(message: str):
    print(f"[DRAG-AND-DROP-SUPPORT] {message}")


def is_agree() -> bool:
    prefs = bpy.context.preferences.addons[__package__].preferences
    return typing.cast(bool, prefs.is_accept)


def try_load():
    global is_load_native_library
    global native_handler

    if is_agree():
        if is_load_native_library:
            log("native library already loaded")
            return

        try:
            dirname = os.path.dirname(__file__)
            native = os.path.join(dirname, "blender-injection.dll")
            native_handler = ctypes.cdll.LoadLibrary(native)
            is_load_native_library = True

            log("loaded native library because agree to security policy")

        except:
            is_load_native_library = False
    else:
        log("did not load native library because not agree to security policy")


def try_unload():
    global is_load_native_library
    global native_handler

    if is_load_native_library:
        import _ctypes

        try:
            _ctypes.FreeLibrary(native_handler._handle)
            log("native library unloaded")

            is_load_native_library = False

        except:
            log("failed to unload native library")
