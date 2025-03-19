from collections.abc import Mapping, Iterable, Sequence
from typing import Any, TypeVar, TYPE_CHECKING

import attrs
from typing_extensions import deprecated

from caqtus.device import DeviceName, DeviceConfiguration
from caqtus.types.timelane import TimeLanes, TimeLane
from caqtus.types.variable_name import DottedVariableName
from .timing import to_time, get_step_bounds, Time
from ..formatter import fmt
from ..types.expression import Expression
from ..types.parameter import NotQuantityError, Parameters
from ..types.recoverable_exceptions import InvalidValueError, EvaluationError
from ..types.units import (
    DimensionalityError,
    InvalidDimensionalityError,
    SECOND,
    is_scalar_quantity,
)

if TYPE_CHECKING:
    from caqtus.shot_compilation import DeviceCompiler

LaneType = TypeVar("LaneType", bound=TimeLane)


@attrs.define(slots=False)
class SequenceContext:
    """Contains information about a sequence being compiled."""

    _device_configurations: Mapping[DeviceName, DeviceConfiguration]
    _time_lanes: TimeLanes

    def get_device_configuration(self, device_name: DeviceName) -> DeviceConfiguration:
        """Returns the configuration for the given device.

        raises:
            KeyError: If no configuration is found for the given device.
        """

        return self._device_configurations[device_name]

    def get_all_device_configurations(self) -> Mapping[DeviceName, DeviceConfiguration]:
        """Returns all device configurations available in this sequence."""

        return self._device_configurations

    def get_lane(self, name: str) -> TimeLane:
        """Returns the time lane with the given name.

        raises:
            KeyError: If no lane with the given name is not found in the sequence
            context.
        """

        return self._time_lanes.lanes[name]

    def get_lanes_with_type(self, lane_type: type[LaneType]) -> Mapping[str, LaneType]:
        """Returns the lanes used during the shot with the given type."""

        return {
            name: lane
            for name, lane in self._time_lanes.lanes.items()
            if isinstance(lane, lane_type)
        }

    def get_step_names(self) -> tuple[str, ...]:
        """Returns the names of the steps in the sequence."""

        return tuple(self._time_lanes.step_names)


@attrs.define
class ShotContext:
    """Contains information about a shot being compiled."""

    _sequence_context: SequenceContext = attrs.field()
    _variables: Mapping[DottedVariableName, Any] = attrs.field()
    _device_compilers: Mapping[DeviceName, "DeviceCompiler"] = attrs.field()

    _step_durations: tuple[Time, ...] = attrs.field(init=False)
    _step_bounds: tuple[Time, ...] = attrs.field(init=False)
    _was_lane_used: dict[str, bool] = attrs.field(init=False)
    _computed_shot_parameters: dict[DeviceName, Mapping[str, Any]] = attrs.field(
        init=False
    )

    @property
    def _time_lanes(self) -> TimeLanes:
        # noinspection PyProtectedMember
        return self._sequence_context._time_lanes

    def __attrs_post_init__(self):
        self._step_durations = tuple(
            evaluate_step_durations(
                self._time_lanes.step_names,
                self._time_lanes.step_durations,
                self._variables,
            )
        )
        self._step_bounds = tuple(get_step_bounds(self._step_durations))
        self._was_lane_used = {name: False for name in self._time_lanes.lanes}
        self._computed_shot_parameters = {}

    def get_lane(self, name: str) -> TimeLane:
        """Returns the lane with the given name for the shot.

        raises:
            KeyError: If no lane with the given name is present for the shot.
        """

        lane = self._sequence_context.get_lane(name)
        self.mark_lane_used(name)

        return lane

    def mark_lane_used(self, name: str) -> None:
        """Signal that a lane was consumed during the shot.

        Raises:
            KeyError: If no lane with the given name is present for the shot.
        """

        self._was_lane_used[name] = True

    def get_lanes_with_type(self, lane_type: type[LaneType]) -> Mapping[str, LaneType]:
        """Returns the lanes used during the shot with the given type."""

        # Unclear if the lanes obtained here should be marked as used or not.
        return self._sequence_context.get_lanes_with_type(lane_type)

    def get_step_names(self) -> tuple[str, ...]:
        """Returns the names of the steps in the shot."""

        return self._sequence_context.get_step_names()

    def get_step_durations(self) -> Sequence[Time]:
        """Returns the durations of each step in seconds."""

        return self._step_durations

    def get_step_start_times(self) -> Sequence[Time]:
        """Returns the times at which each step starts.

        Returns:
            A sequence representing the start times of each step in seconds.

            For steps with durations [d_0, d_1, ..., d_(n-1)], the returned values are
            [0, d_0, d_0 + d_1, ..., d_0 + ... + d_(n-1)].

            The returned sequence has one more element than the number of steps.
            The last element is the total duration of the shot.
        """

        return self._step_bounds

    @deprecated("Use get_step_start_times instead")
    def get_step_bounds(self) -> Sequence[Time]:
        return self.get_step_start_times()

    def get_shot_duration(self) -> Time:
        """Returns the total duration of the shot in seconds."""

        return self._step_bounds[-1]

    def get_parameters(self) -> Parameters:
        """Returns the parameters that define the shot."""

        return self._variables

    @deprecated("Use get_parameters instead", stacklevel=2)
    def get_variables(self) -> Mapping[DottedVariableName, Any]:
        return self.get_parameters()

    def get_device_config(self, device_name: DeviceName) -> DeviceConfiguration:
        """Returns the configuration for the given device.

        raises:
            KeyError: If no configuration is found for the given device.
        """

        return self._sequence_context.get_device_configuration(device_name)

    def get_device_compiler(self, device_name: DeviceName) -> "DeviceCompiler":
        """Returns the device compiler for the given device name.

        Raises:
            KeyError: If the requested device is not in use for the current shot.
        """

        return self._device_compilers[device_name]

    def get_shot_parameters(self, device_name: DeviceName) -> Mapping[str, Any]:
        """Returns the parameters computed for the given device."""

        if device_name in self._computed_shot_parameters:
            return self._computed_shot_parameters[device_name]
        else:
            compiler = self._device_compilers[device_name]
            try:
                shot_parameters = compiler.compile_shot_parameters(self)
            except Exception as e:
                raise DeviceCompilationError(
                    fmt(
                        "Couldn't compile parameters for {:device}",
                        device_name,
                    )
                ) from e
            self._computed_shot_parameters[device_name] = shot_parameters
            return shot_parameters

    def _unused_lanes(self) -> set[str]:
        return {name for name, used in self._was_lane_used.items() if not used}


class DeviceCompilationError(Exception):
    """Raised when compilation for a device fails."""

    pass


def evaluate_step_durations(
    step_names: Iterable[str],
    step_durations: Iterable[Expression],
    variables: Mapping[DottedVariableName, Any],
) -> list[Time]:
    result = []

    for step, (name, duration) in enumerate(
        zip(step_names, step_durations, strict=True)
    ):
        try:
            evaluated = duration.evaluate(variables)
        except EvaluationError as e:
            raise EvaluationError(
                fmt(
                    "Couldn't evaluate {:expression} for duration of {:step}",
                    duration,
                    (step, name),
                )
            ) from e

        if not is_scalar_quantity(evaluated):
            raise NotQuantityError(
                fmt(
                    "{:expression} for duration of {:step} does not evaluate "
                    "to a scalar quantity",
                    duration,
                    (step, name),
                )
            )

        try:
            seconds = evaluated.to_unit(SECOND).magnitude
        except DimensionalityError as error:
            raise InvalidDimensionalityError(
                fmt(
                    "Couldn't convert {:expression} for duration of {:step} to "
                    "seconds",
                    duration,
                    (step, name),
                )
            ) from error
        if seconds < 0:
            raise InvalidValueError(
                fmt(
                    "{:expression} for duration of {:step} is negative",
                    duration,
                    (step, name),
                )
            )
        result.append(to_time(seconds))
    return result
