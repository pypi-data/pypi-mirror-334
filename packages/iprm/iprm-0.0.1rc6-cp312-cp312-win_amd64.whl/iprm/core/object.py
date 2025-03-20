"""
Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>

SPDX-License-Identifier: MIT
"""
from iprm.core.core import Object as _Object
from contextlib import contextmanager
from typing import Any, Optional

_object_created_callback: Optional[callable] = None


@contextmanager
def object_created_callback(on_object_created: callable):
    global _object_created_callback
    _object_created_callback = on_object_created
    try:
        yield
    finally:
        _object_created_callback = None


class Object(_Object):
    def __init__(self, name: str):
        super().__init__(name)
        from iprm.core.session import Session
        Session.register_object(self)
        # TODO: Working around the issues with trying to get the python layer to
        #  directly receive/work with the core c++ layer, as when I initially switched
        #  to that to avoid registering callbacks in the core, it then broke all
        #  type/inheritance information. Must be a way around this, but this is good
        #  enough for now and more or less what I had initially, just not nested
        #  all the way down in the core, so we can live with it for now
        if _object_created_callback is not None:
            _object_created_callback(self)
        self.properties: dict[str, Any] = {}
