from anyio._backends._asyncio import AsyncIOBackend, WorkerThread
from anyio._core._eventloop import claim_worker_thread, threadlocals
from django.db import close_old_connections


class CustomWorkerThread(WorkerThread):
    """
    AnyIO thread worker modified for correct close db connection.

    """

    def run(self) -> None:
        with claim_worker_thread(AsyncIOBackend, self.loop):
            while True:
                item = self.queue.get()
                if item is None:
                    return

                context, func, args, future, cancel_scope = item
                if not future.cancelled():
                    result = None
                    exception: BaseException | None = None
                    threadlocals.current_cancel_scope = cancel_scope
                    try:
                        result = context.run(func, *args)
                    except BaseException as exc:
                        exception = exc
                    finally:
                        del threadlocals.current_cancel_scope
                        close_old_connections()

                    if not self.loop.is_closed():
                        self.loop.call_soon_threadsafe(self._report_result, future, result, exception)

                self.queue.task_done()
