"""This module contains the :class:`DeviceConfiguration` class."""

from __future__ import annotations

from collections.abc import Mapping
from typing import (
    TypeVar,
    Optional,
    NewType,
    Generic,
)

import attrs

from caqtus.device.runtime import Device
from caqtus.types.data import DataType, DataLabel
from caqtus.types.parameter import ParameterSchema
from caqtus.types.timelane import TimeLanes

DeviceServerName = NewType("DeviceServerName", str)

DeviceType = TypeVar("DeviceType", bound=Device)


@attrs.define
class DeviceConfiguration(Generic[DeviceType]):
    """Contains static information about a device.

    This is an abstract class, generic in :data:`DeviceType` that stores the information
    necessary to connect to a device and program it during a sequence.

    This information is meant to be encoded in a user-friendly way that might not be
    possible to be directly programmed on a device.
    For example, it might contain not yet evaluated
    :class:`caqtus.types.expression.Expression` objects that only make sense in the
    context of a shot.

    Subclasses should add necessary attributes depending on the device.

    The dunder method :meth:`__eq__` should be implemented.

    Attributes:
        remote_server: Indicates the name of the computer on which the device should be
            instantiated.
    """

    remote_server: Optional[DeviceServerName] = attrs.field()

    def get_data_schema(
        self, parameter_schema: ParameterSchema, time_lanes: TimeLanes
    ) -> Mapping[DataLabel, DataType]:
        return {}


DeviceConfigType = TypeVar("DeviceConfigType", bound=DeviceConfiguration)
