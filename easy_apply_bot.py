"""Backward-compatible entrypoint.

The implementation has been moved into the `linkedin_easy_apply` package.
Use this file as the runtime entrypoint to preserve existing workflows.
"""

from linkedin_easy_apply.bot import EasyApplyBot
from linkedin_easy_apply.runner import main

__all__ = ["EasyApplyBot", "main"]


if __name__ == "__main__":
    main()
