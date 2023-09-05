import aiohttp
import asyncio
import threading
import queue
import uproot

class AIOHTTPSource(uproot.source.chunk.Source):
    """
    Experimental data source for uproot with asyncio and connection pooling using the aiohttp module.
    The event loop runs in a separate thread.
    """
    def __init__(self, file_path, ssl_context=None, tcp_connection_limit=10, **options):
        self._file_path = file_path
        self._ssl_context = ssl_context
        self._tcp_connection_limit = tcp_connection_limit

        def run_loop(loop, q):
            asyncio.set_event_loop(loop)
            exit_event = asyncio.Event()
            q.put(exit_event)

            async def wait_for_event(event):
                await event.wait()

            loop.run_until_complete(wait_for_event(exit_event))

        self._loop = asyncio.new_event_loop()
        q = queue.Queue()
        self._aio_thread = threading.Thread(target=run_loop, args=(self._loop, q), daemon=True)
        self._aio_thread.start()
        self._aio_exit_event = q.get()

        async def create_session():
            conn = aiohttp.TCPConnector(limit=self._tcp_connection_limit)
            return aiohttp.ClientSession(connector=conn)

        self._session = self._submit_async(create_session()).result()

    def _submit_async(self, coro):
        "Run coroutine in the event loop in the other thread"
        return asyncio.run_coroutine_threadsafe(coro, self._loop)

    @property
    def closed(self):
        return self._session.closed

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        async def stop(event):
            event.set()

        self._submit_async(self._session.close()).result()
        self._submit_async(stop(self._aio_exit_event)).result()
        self._aio_thread.join()

    async def get(self, start, stop, notifications=None):
        async with self._session.get(
            self._file_path,
            headers={"Range": f"bytes={start}-{stop - 1}"},
            ssl=self._ssl_context,
        ) as resp:
            content = await resp.read()
            future = uproot.source.futures.TrivialFuture(content)
            chunk = uproot.source.chunk.Chunk(self, start, stop, future)
            if notifications is not None:
                notifications.put(chunk)
            return chunk

    def chunk(self, start, stop):
        return self._submit_async(self.get(start, stop)).result()

    def chunks(self, ranges, notifications):

        async def achunks():
            return await asyncio.gather(
                *[self.get(start, stop, notifications) for start, stop in ranges]
            )

        return self._submit_async(achunks()).result()
