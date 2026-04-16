import asyncio
from src.loader import build_application, configure_logging


def main() -> None:
    configure_logging()
    app = build_application()
    # Python 3.14 da default event loop avtomatik yaratilmaydi.
    asyncio.set_event_loop(asyncio.new_event_loop())
    app.run_polling(allowed_updates=None)


if __name__ == "__main__":
    main()
