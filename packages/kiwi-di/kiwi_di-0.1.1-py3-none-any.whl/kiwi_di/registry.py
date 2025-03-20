import dataclasses
import logging
from copy import deepcopy
from typing import Any, Iterable

from data_types import ComponentMetadata, NO_DEFAULT_VALUE
from exceptions import AmbiguousEntityError
from singleton import Singleton

logger = logging.getLogger("easydi")

@dataclasses.dataclass(frozen=True)
class _ComponentId:
    name: str
    qualifier: str


@dataclasses.dataclass(frozen=True)
class _WaitingListItem:
    metadata: ComponentMetadata
    waiting_on: set[_ComponentId]


class ComponentRegistry(metaclass=Singleton):
    
    def __init__(self):
        self._component_metadata: dict[_ComponentId, ComponentMetadata] = {}
        self._component_instances: dict[_ComponentId, Any] = {}
        self._config_values: dict[str, Any] = {}
    
        self._waiting_list: dict[_ComponentId, _WaitingListItem] = {}
        self._signal_dict: dict[_ComponentId, set[_ComponentId]] = {}

    def get_instance(self, component_id: _ComponentId) -> Any:
        return self._component_instances.get(component_id)

    def components(self) -> dict[_ComponentId, ComponentMetadata]:
        return deepcopy(self._component_metadata)

    def register_component(self, component_metadata: ComponentMetadata) -> None:
        component_id = _ComponentId(
            name=component_metadata.name,
            qualifier=component_metadata.qualifier
        )
        if component_id in self._component_metadata:
            raise AmbiguousEntityError(name=component_id.name, qualifier=component_id.qualifier)

        logger.debug("Registering component %s", component_metadata)
        self._component_metadata[component_id] = component_metadata

    def load_config_values(self) -> None:
        raise NotImplementedError()

    def wire_components(self) -> None:
        for component_id, metadata in self._component_metadata.items():
            if component_id not in self._component_instances:
                self._try_instantiate_component(component_id, metadata)
        # TODO(Kaiyu): Throw when some components cannot be instantiated
        logger.debug("All component instantiated.")

    def _try_instantiate_component(self, component_id: _ComponentId, metadata: ComponentMetadata) -> None:
        if len(metadata.parameters) == 0:
            logger.debug("Instantiating %s with no parameters", component_id)
            self._instantiate(component_id, metadata, {})
            return

        param_values: dict[str, Any] = {}
        unresolved_params: dict[str, _ComponentId] = {}

        for param in metadata.parameters:
            if param.default_value != NO_DEFAULT_VALUE:
                param_values[param.name] = param.default_value
                continue

            # TODO(Kaiyu): Get from config values

            param_component_id = _ComponentId(name=param.type, qualifier=param.qualifier)
            if param_component_id in self._component_instances:

                param_values[param.name] = self._component_instances[param_component_id]
                continue

            unresolved_params[param.name] = param_component_id

        if len(unresolved_params) == 0:
            logger.debug("Instantiating %s with all its parameters", component_id)
            self._instantiate(component_id, metadata, param_values)
        else:
            logger.debug("Put %s on waiting list, waiting on %s", component_id, unresolved_params)
            self._waiting_list[component_id] = _WaitingListItem(
                metadata=metadata, waiting_on=set(unresolved_params.values())
            )
            self._add_to_signal_dict(component_id, unresolved_params.values())

    def _instantiate(self, component_id: _ComponentId, metadata: ComponentMetadata, param_values: dict[str, Any]) -> None:
        instance = metadata.instantiate_func(**param_values)

        self._component_instances[component_id] = instance
        if component_id in self._waiting_list:
            self._waiting_list.pop(component_id)
        self._signal_waiting_list(instantiated_component=component_id)

        for super_class in metadata.super_classes:
            super_class_id = _ComponentId(name=super_class, qualifier=metadata.qualifier)
            self._component_instances[super_class_id] = instance
            self._signal_waiting_list(instantiated_component=super_class_id)

    def _add_to_signal_dict(self, component_id: _ComponentId, unresolved_params: Iterable[_ComponentId]) -> None:
        for param_component_id in unresolved_params:
            if param_component_id in self._signal_dict:
                self._signal_dict[param_component_id].add(component_id)
            else:
                self._signal_dict[param_component_id] = {component_id}

    def _signal_waiting_list(self, instantiated_component: _ComponentId) -> None:
        if instantiated_component not in self._signal_dict:
            return
        for component_to_signal in self._signal_dict[instantiated_component]:
            if (component_to_signal in self._waiting_list
                and instantiated_component in self._waiting_list[component_to_signal].waiting_on):
                self._try_instantiate_component(
                    component_id=component_to_signal,
                    metadata=self._waiting_list[component_to_signal].metadata
                )