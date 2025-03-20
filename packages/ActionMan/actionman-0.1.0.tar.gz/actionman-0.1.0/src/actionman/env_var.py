"""Work with environment variables in a GitHub Actions workflow."""

from typing import Type as _Type
import os as _os
from pathlib import Path as _Path
import json as _json

from actionman import _format
from actionman.exception import (
    ActionManGitHubError as _ActionManGitHubError,
    ActionManInputVariableDeserializationError as _ActionManInputVariableDeserializationError,
    ActionManInputVariableTypeError as _ActionManInputVariableTypeError,
    ActionManInputVariableTypeMismatchError as _ActionManInputVariableTypeMismatchError,
)


_ENV_VAR_NAME = "GITHUB_ENV"
_FILEPATH: _Path | None = _Path(_os.environ[_ENV_VAR_NAME]) if _ENV_VAR_NAME in _os.environ else None


def read(
    name: str,
    typ: _Type[str | bool | int | float | list | dict] = str,
) -> str | bool | int | float | list | dict | None:
    """Read an environment variable and cast it to the given type.

    Parameters
    ----------
    name : str
        The name of the environment variable to read.
    typ : Type[str | bool | int | float | list | dict], default: str
        The type to cast the environment variable to.
        If the type is not str, the value of the environment variable
        is expected to be a JSON string that can be deserialized to the given type.

    Returns
    -------
    str | bool | int | float | list | dict | None
        The value of the environment variable cast to the given type.
        If the environment variable is not set, None is returned.

    Raises
    ------
    actionman.exception.ActionManInputVariableTypeError
        If the specified type is not supported.
    actionman.exception.ActionManInputVariableDeserializationError
        If the environment variable could not be deserialized.
    actionman.exception.ActionManInputVariableTypeMismatchError
        If the deserialized environment variable has a type other than the specified type.
    """
    if typ not in (str, bool, int, float, list, dict):
        raise _ActionManInputVariableTypeError(var_name=name, var_type=typ)
    value = _os.environ.get(name)
    if value is None:
        return
    if typ is str:
        return value
    try:
        value_deserialized = _json.loads(value)
    except Exception as e:
        raise _ActionManInputVariableDeserializationError(
            var_name=name,
            var_value=value,
            var_type=typ,
            exception=e
        ) from e
    if not isinstance(value_deserialized, typ):
        raise _ActionManInputVariableTypeMismatchError(
            var_name=name,
            var_value=value_deserialized,
            var_type=typ
        )
    return value_deserialized


def write(name: str, value: dict | list | tuple | str | bool | int | float | None) -> str:
    """Set a persistent environment variable
    that is available to all subsequent steps in the current job.

    This is done by writing the environment variable
    to the environment file whose path is specified by the 'GITHUB_ENV' environment variable.

    Parameters
    ----------
    name : str
        The name of the output parameter.
    value : dict | list | tuple | str | bool | int | float | None
        The value of the output parameter.
        If the value is not a string, it will be serialized and written as a JSON string.

    Returns
    -------
    str
        The output that was written to the file.
        This is only useful for logging/debugging purposes.

    Raises
    ------
    actionman.exception.ActionManGitHubError
        If the 'GITHUB_ENV' environment variable is not set.
    actionman.exception.ActionManOutputVariableTypeError
        If the value has an unsupported type.
    actionman.exception.ActionManOutputVariableSerializationError
        If the value could not be serialized to a JSON string.

    References
    ----------
    - [GitHub Docs: Workflow Commands for GitHub Actions: Setting an environment variable](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-environment-variable)
    """
    if not _FILEPATH:
        raise _ActionManGitHubError(missing_env_var=_ENV_VAR_NAME)
    output = _format.output_variable(key=name, value=value)
    with open(_FILEPATH, "a") as f:
        print(output, file=f)
    return output
