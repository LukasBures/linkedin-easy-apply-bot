"""Backward-compatible import wrapper for application runner."""

from .app.runner import main, run_from_config

__all__ = ["main", "run_from_config"]
