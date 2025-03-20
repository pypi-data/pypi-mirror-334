"""Work with the step summary of the current step of a job run in a GitHub Actions workflow.

References
----------
- [GitHub Docs: Workflow Commands for GitHub Actions: Adding a job summary](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary)
"""

from __future__ import annotations as _annotations
from typing import TYPE_CHECKING as _TYPE_CHECKING
import os as _os
from pathlib import Path as _Path

from actionman.exception import ActionManGitHubError as _ActionManGitHubError

if _TYPE_CHECKING:
    from protocolman import Stringable


_ENV_VAR_NAME = "GITHUB_STEP_SUMMARY"
_FILEPATH: _Path | None = _Path(_os.environ[_ENV_VAR_NAME]) if _ENV_VAR_NAME in _os.environ else None


def filepath() -> _Path:
    """Get the path to the file where the step summary is stored.

    Raises
    ------
    actionman.exception.ActionManGitHubError
        If the 'GITHUB_STEP_SUMMARY' environment variable is not set.
    """
    if not _FILEPATH:
        raise _ActionManGitHubError(missing_env_var=_ENV_VAR_NAME)
    return _FILEPATH


def read() -> str | None:
    """Read the current step summary contents from the file.

    Raises
    ------
    actionman.exception.ActionManGitHubError
        If the 'GITHUB_STEP_SUMMARY' environment variable is not set.
    """
    if not _FILEPATH:
        raise _ActionManGitHubError(missing_env_var=_ENV_VAR_NAME)
    return _FILEPATH.read_text() if _FILEPATH.is_file() else None


def append(content: Stringable) -> None:
    """Append the given content to the step summary file.

    Raises
    ------
    actionman.exception.ActionManGitHubError
        If the 'GITHUB_STEP_SUMMARY' environment variable is not set.
    """
    if not _FILEPATH:
        raise _ActionManGitHubError(missing_env_var=_ENV_VAR_NAME)
    with open(_FILEPATH, "a") as f:
        print(content, file=f)
    return


def write(content: Stringable) -> None:
    """Overwrite the step summary file with the given content.

    Raises
    ------
    actionman.exception.ActionManGitHubError
        If the 'GITHUB_STEP_SUMMARY' environment variable is not set.
    """
    if not _FILEPATH:
        raise _ActionManGitHubError(missing_env_var=_ENV_VAR_NAME)
    with open(_FILEPATH, "w") as f:
        print(content, file=f)
    return


def remove() -> None:
    """Remove all step summary contents by deleting the file.

    Raises
    ------
    actionman.exception.ActionManGitHubError
        If the 'GITHUB_STEP_SUMMARY' environment variable is not set.
    """
    if not _FILEPATH:
        raise _ActionManGitHubError(missing_env_var=_ENV_VAR_NAME)
    _FILEPATH.unlink()
    return
