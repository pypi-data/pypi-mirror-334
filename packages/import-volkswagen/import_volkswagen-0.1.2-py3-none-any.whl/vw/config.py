"""Configuration variables for vw."""

import pathlib
import typing

import decouple as _decouple

_cwd = pathlib.Path.cwd()

_decouple_config = _decouple.AutoConfig(search_path=_cwd)

_vm_ignore_value = _decouple_config("VW_IGNORE", default="")
VW_IGNORE: typing.Optional[bool] = (
    (_vm_ignore_value.lower() in {"1", "t", "true"}) if _vm_ignore_value else None
)
"""If set, this value can be used to specify to ignore whether in a testing environment or not."""

_vm_always_value = _decouple_config("VW_ALWAYS", default="")
VW_ALWAYS: typing.Optional[bool] = (
    (_vm_always_value.lower() in {"1", "t", "true"}) if _vm_always_value else None
)
"""If set, this value causes all methods to behave as if in a testing environment."""
