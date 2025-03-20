"""ActionMan: GitHub Actions utilities for Python."""

import io as _io
import sys as _sys

from actionman import log, env_var, step_output, step_summary


def in_gha() -> bool:
    """Check whether the current program is running in a GitHub Actions environment.

    This is done by checking the presence of the 'GITHUB_ACTIONS' environment variable.

    References
    ----------
    - [GitHub Docs: Default environment variables](https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/store-information-in-variables#default-environment-variables)
    """
    return bool(env_var.read("GITHUB_ACTIONS", bool))


if hasattr(_sys.stdout, 'buffer'):
    # Wrap the standard output stream to change its encoding to UTF-8,
    # which is required for writing unicode characters (e.g., emojis) to the console in Windows.
    # However, this works in standard Python environments where sys.stdout is a regular file object;
    # in environments like Jupyter, sys.stdout is already set up to handle Unicode,
    # and does not need to be (and cannot be) wrapped in this way.
    _sys.stdout = _io.TextIOWrapper(_sys.stdout.buffer, encoding='utf-8')
