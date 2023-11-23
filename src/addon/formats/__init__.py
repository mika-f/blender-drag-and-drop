# ------------------------------------------------------------------------------------------
#  Copyright (c) Natsuneko. All rights reserved.
#  Licensed under the MIT License. See LICENSE in the project root for license information.
# ------------------------------------------------------------------------------------------

# pyright: reportUnusedImport=false

from . import abc
from . import bvh
from . import dae
from . import fbx
from . import glb
from . import obj
from . import obj_legacy
from . import vrm

CLASSES: list[type] = []
CLASSES.extend(abc.OPERATORS)
CLASSES.extend(bvh.OPERATORS)
CLASSES.extend(dae.OPERATORS)
CLASSES.extend(fbx.OPERATORS)
CLASSES.extend(glb.OPERATORS)
CLASSES.extend(obj_legacy.OPERATORS)
CLASSES.extend(obj.OPERATORS)
CLASSES.extend(vrm.OPERATORS)
