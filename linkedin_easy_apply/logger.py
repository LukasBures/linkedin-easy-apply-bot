"""Backward-compatible import wrapper for logger."""

from .observability.logger import log, setup_logger

__all__ = ["log", "setup_logger"]
