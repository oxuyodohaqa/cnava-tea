"""Lightweight entrypoint that delegates to the main bot module."""

from tg import add_super_admin_command, main

__all__ = ["main", "add_super_admin_command"]


if __name__ == "__main__":
    main()
