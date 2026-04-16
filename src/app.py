from src.loader import build_application, configure_logging


def main() -> None:
    configure_logging()
    app = build_application()
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
