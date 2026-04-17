import asyncio
import os
from contextlib import suppress

from src.loader import build_application, configure_logging


async def _health_server() -> None:
    async def _handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            await reader.read(1024)
            body = b"OK"
            response = (
                b"HTTP/1.1 200 OK\r\n"
                b"Content-Type: text/plain; charset=utf-8\r\n"
                b"Content-Length: 2\r\n"
                b"Connection: close\r\n\r\n"
                + body
            )
            writer.write(response)
            await writer.drain()
        finally:
            writer.close()
            with suppress(Exception):
                await writer.wait_closed()

    port = int(os.environ.get("PORT", "10000"))
    server = await asyncio.start_server(_handle_client, host="0.0.0.0", port=port)
    async with server:
        await server.serve_forever()


async def main() -> None:
    configure_logging()
    app = build_application()
    await app.initialize()
    await app.start()

    health_task = asyncio.create_task(_health_server())
    polling_task = asyncio.create_task(
        app.updater.start_polling(allowed_updates=None, drop_pending_updates=True)
    )

    try:
        await polling_task
        await asyncio.Event().wait()
    finally:
        health_task.cancel()
        polling_task.cancel()
        with suppress(asyncio.CancelledError):
            await health_task
        with suppress(asyncio.CancelledError):
            await polling_task
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
