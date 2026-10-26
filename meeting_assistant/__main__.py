"""Keep the previous Python launch command working after the Zenith rename."""

from zenith.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
