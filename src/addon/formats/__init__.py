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
from . import ply
from . import stl
from . import stl_legacy
from . import svg
from . import usd
from . import vrm
from . import x3d

CLASSES: list[type] = []

# legacy importers
CLASSES.extend(obj_legacy.OPERATORS)
CLASSES.extend(stl_legacy.OPERATORS)

# modern importers
CLASSES.extend(abc.OPERATORS)
CLASSES.extend(bvh.OPERATORS)
CLASSES.extend(dae.OPERATORS)
CLASSES.extend(fbx.OPERATORS)
CLASSES.extend(glb.OPERATORS)
CLASSES.extend(obj.OPERATORS)
CLASSES.extend(ply.OPERATORS)
CLASSES.extend(stl.OPERATORS)
CLASSES.extend(svg.OPERATORS)
CLASSES.extend(usd.OPERATORS)
CLASSES.extend(vrm.OPERATORS)
CLASSES.extend(x3d.OPERATORS)
