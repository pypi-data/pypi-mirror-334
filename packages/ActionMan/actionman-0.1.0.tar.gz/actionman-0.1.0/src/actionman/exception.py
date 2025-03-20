"""Exceptions raised by ActionMan."""


from typing import Any as _Any, Type as _Type


class ActionManError(Exception):
    """Base class for all ActionMan errors."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
        return


class ActionManGitHubError(ActionManError):
    """The package was initialized from outside GitHub, and the required environment variables are not set."""

    def __init__(self, missing_env_var: str):
        message = (
            f"The package was initialized from outside GitHub, "
            f"as the required environment variable '{missing_env_var}' is not set."
        )
        super().__init__(message)
        self.missing_environment_variable: str = missing_env_var
        return


class ActionManVariableError(ActionManError):
    """Base class for all ActionMan variable errors."""

    def __init__(self, var_name: _Any, message: str):
        super().__init__(message)
        self.variable_name = var_name
        return


class ActionManInputVariableError(ActionManVariableError):
    """Base class for all ActionMan input variable errors."""

    def __init__(self, var_name: str, message: str):
        super().__init__(var_name=var_name, message=message)
        return


class ActionManOutputVariableError(ActionManVariableError):
    """Base class for all ActionMan output variable errors."""

    def __init__(self, var_name: str, var_value: _Any, message: str):
        super().__init__(var_name=var_name, message=message)
        self.variable_value = var_value
        return


class ActionManInputVariableTypeError(ActionManInputVariableError):
    """An input variable has an unsupported type."""

    def __init__(self, var_name: str, var_type: _Any):
        message = (
            f"Input variable '{var_name}' has an unsupported expected type '{var_type.__name__}'."
        )
        super().__init__(var_name=var_name, message=message)
        return


class ActionManInputVariableTypeMismatchError(ActionManInputVariableError):
    """An input variable has a type other than its expected type."""

    def __init__(self, var_name: str, var_value: str | bool | int | float | list | dict, var_type: _Any):
        message = (
            f"Input variable '{var_name}' has type '{type(var_value).__name__}', "
            f"but expected type {var_type.__name__}."
        )
        super().__init__(var_name=var_name, message=message)
        self.variable_value = var_value
        self.variable_type = var_type
        return


class ActionManInputVariableDeserializationError(ActionManInputVariableError):
    """An input variable could not be deserialized from a JSON string."""

    def __init__(
        self,
        var_name: str,
        var_value: str,
        var_type: _Type[bool | int | float | list | dict],
        exception: Exception
    ):
        message = (
            f"Failed to deserialize input variable '{var_name}' with expected type '{var_type.__name__}' "
            f"from a JSON string; {str(exception).removesuffix('.')}."
        )
        super().__init__(var_name=var_name, message=message)
        self.variable_value = var_value
        self.variable_type = var_type
        return


class ActionManOutputVariableSerializationError(ActionManOutputVariableError):
    """An output variable could not be serialized to a JSON string."""

    def __init__(self, var_name: str, var_value: _Any, exception: Exception):
        message = (
            f"Failed to serialize output variable '{var_name}' with type '{type(var_value).__name__}' "
            f"to a JSON string; {str(exception).removesuffix('.')}."
        )
        super().__init__(var_name=var_name, var_value=var_value, message=message)
        return


class ActionManOutputVariableTypeError(ActionManOutputVariableError):
    """An output variable has an unsupported type."""

    def __init__(self, var_name: str, var_value: _Any):
        message = (
            f"Output variable '{var_name}' has an unsupported type '{type(var_value).__name__}'."
        )
        super().__init__(var_name=var_name, var_value=var_value, message=message)
        return
