import abc
import inspect
import typing

from typing import Callable, Annotated, Any

from data_types import Parameter, ComponentMetadata, Qualifier, DEFAULT_QUALIFIER, NO_DEFAULT_VALUE, NO_QUALIFIER
from registry import ComponentRegistry, _ComponentId
from exceptions import UnspecifiedParameterTypeError, InjectError

T = typing.TypeVar('T')


def component(_component: T) -> T:
    entity_metadata = _get_metadata(
        _component=_component,
        component_qualifier=DEFAULT_QUALIFIER
    )
    ComponentRegistry().register_component(entity_metadata)
    return _component


def named_component(qualifier: str = DEFAULT_QUALIFIER) -> T:
    def decorator(_component: T) -> T:
        entity_metadata = _get_metadata(
            _component=_component,
            component_qualifier=qualifier
        )
        ComponentRegistry().register_component(entity_metadata)
        return _component
    return decorator

def inject(func: Callable[[...], T]) -> Callable[[], T]:
    registry = ComponentRegistry()
    registry.wire_components()
    func_metadata = _get_metadata(func, component_qualifier=NO_QUALIFIER)

    unresolved_params = []
    instantiated_params = {}
    for param in func_metadata.parameters:
        if param.default_value != NO_DEFAULT_VALUE:
            instantiated_params[param.name] = param.default_value
            continue

        param_component_id = _ComponentId(name=param.type, qualifier=param.qualifier)
        param_instance = registry.get_instance(param_component_id)
        if param_instance is None:
            unresolved_params.append(param)
        else:
            instantiated_params[param.name] = param_instance

    if len(unresolved_params) > 0:
        raise InjectError(
            f"Cannot inject to function {func.__name__},"
            "no @component or @named_component decorated class"
            f"found for parameters {unresolved_params}."
        )

    return lambda : func(**instantiated_params)


def _get_metadata(_component: Any, component_qualifier: str) -> ComponentMetadata:
    component_name = _get_fullname(_component)

    signature = inspect.signature(_component)
    parameters = _get_params(component_name, signature)
    return_type = signature.return_annotation if signature.return_annotation != signature.empty else None
    super_classes = _get_super_classes(_component)

    return ComponentMetadata(
        name=component_name,
        parameters=parameters,
        return_type=return_type,
        qualifier=component_qualifier,
        instantiate_func=_component,
        super_classes=super_classes
    )


def _get_params(component_name, signature):
    params_set = set()
    for param in signature.parameters.values():
        if param.annotation is param.empty:
            raise UnspecifiedParameterTypeError(
                component_name=component_name,
                param_name=param.name
            )

        param_annotation = param.annotation
        param_qualifier = DEFAULT_QUALIFIER

        if typing.get_origin(param_annotation) is Annotated:
            args = typing.get_args(param_annotation)
            _type = args[0]
            hint = args[1]
            if isinstance(hint, Qualifier):
                param_annotation = _type
                param_qualifier = hint.name

        params_set.add(
            Parameter(
                name=param.name,
                type=_get_fullname(param_annotation),
                default_value=param.default if param.default is not param.empty else NO_DEFAULT_VALUE,
                qualifier=param_qualifier
            )
        )
    return params_set


def _get_super_classes(_component: Any) -> list[str]:
    ret = []
    if hasattr(_component, "__mro__"):
        for clazz in inspect.getmro(_component)[1:]:
            if clazz not in {abc.ABC, object}:
                ret.append(_get_fullname(clazz))
    return ret


def _get_fullname(_component: Any) -> str:
    return f"{_component.__module__}.{_component.__name__}"