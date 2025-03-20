class UnspecifiedParameterTypeError(RuntimeError):

    def __init__(self, component_name: str, param_name: str) -> None:
        super().__init__(
            f"Cannot wire class/function {component_name}, parameter type is not specified for {param_name}."
        )


class AmbiguousEntityError(RuntimeError):

    def __init__(self, name: str, qualifier: str) -> None:
        super().__init__(
            f"More than one {name} with {qualifier} found."
        )


class InjectError(RuntimeError):
    pass
