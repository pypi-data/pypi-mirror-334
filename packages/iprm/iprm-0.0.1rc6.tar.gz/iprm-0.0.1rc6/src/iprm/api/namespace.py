"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.util.env import Env
from iprm.util.dir import CurrentSourceDir, SourceDir, RootRelativeSourceDir
from iprm.api.obj.project import Project
from iprm.api.obj.subdirectories import SubDirectories
from iprm.api.obj.cxx import CXXTarget
from iprm.api.obj.rust import RustTarget

NAMESPACE = {
    # Utilities
    Env.__name__: Env,
    CurrentSourceDir.__name__: CurrentSourceDir,
    SourceDir.__name__: SourceDir,
    RootRelativeSourceDir.__name__: RootRelativeSourceDir,

    # Objects
    Project.__name__: Project,
    SubDirectories.__name__: SubDirectories,
    CXXTarget.__name__: CXXTarget,
    RustTarget.__name__: RustTarget,
}
