"""Work with the step output of the current step of a job run in a GitHub Actions workflow.

References
----------
- [GitHub Docs: Workflow Commands for GitHub Actions: Setting an output parameter](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#setting-an-output-parameter)
"""

import os as _os
from pathlib import Path as _Path

from actionman import _format
from actionman.exception import ActionManGitHubError as _ActionManGitHubError


_ENV_VAR_NAME = "GITHUB_OUTPUT"
_FILEPATH: _Path | None = _Path(_os.environ[_ENV_VAR_NAME]) if _ENV_VAR_NAME in _os.environ else None


def write(name: str, value: dict | list | tuple | str | bool | int | float | None) -> str:
    """Set an output parameter for the current step.

    This is done by writing the output
    to the environment file whose path is specified by the 'GITHUB_OUTPUT' environment variable.

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
        If the 'GITHUB_OUTPUT' environment variable is not set.
    actionman.exception.ActionManOutputVariableTypeError
        If the value has an unsupported type.
    actionman.exception.ActionManOutputVariableSerializationError
        If the value could not be serialized to a JSON string.
    """
    if not _FILEPATH:
        raise _ActionManGitHubError(missing_env_var=_ENV_VAR_NAME)
    output = _format.output_variable(key=name, value=value)
    with open(_FILEPATH, "a") as f:
        print(output, file=f)
    return output
