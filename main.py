import sys

from app.controllers import LavaJatoApp


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    LavaJatoApp().executar()


if __name__ == "__main__":
    main()
