import os
import asyncio
import inspect
import logging
from .client import AsyncClient, SyncClient
from .connection import Connection
from .credentials import TLSCredentials
from .formatter import Formatter

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("DEBUG_LEVEL", "INFO").upper())

class Publisher:
    class Task:
        def __init__(self, scope: "Publisher", function: callable, *, timeout: float=10.0):
            self.scope = scope
            self.fn = function
            self.timeout: float = timeout
            self._lock: asyncio.Lock = asyncio.Lock()

    class AsyncTask(Task):
        def __init__(self, *args, **kwds):
            super().__init__(*args, **kwds)
            
        async def __call__(self, *args, **kwds):
            logger.debug(f"Calling {self.fn.__name__}.")
            result = await self.fn(*args, **kwds)
            scope = self.scope
            try:
                async with self._lock:
                    async with scope as client:
                        recognized_kwargs = inspect.signature(client.publish).parameters.keys()
                        kwargs = {k: v for k, v in scope.kwargs.items() if k in recognized_kwargs}
                        await client.publish(scope.topic,
                                             payload=scope.formatter.pack(result),
                                             **kwargs)
                    logger.debug(f"Published {result}.")
            except Exception as e:
                logger.warning(f"Failed to publish {result} ({type(result)}) to {scope.topic}: {e}")
            return result
            
    class SyncTask(Task):
        def __init__(self, *args, **kwds):
            super().__init__(*args, **kwds)

        def __call__(self, *args, **kwds):
            logger.debug(f"Calling {self.fn.__name__}.")
            result = self.fn(*args, **kwds)
            scope = self.scope
            try:
                with scope as client:
                    recognized_kwargs = inspect.signature(client.publish).parameters.keys()
                    kwargs = {k: v for k, v in scope.kwargs.items() if k in recognized_kwargs}
                    info = client.publish(scope.topic,
                                          scope.formatter.pack(result),
                                          **kwargs)
                    info.wait_for_publish(self.timeout)
                logger.debug(f"Published {result}.")
            except Exception as e:
                logger.warning(f"Failed to publish {result} to {scope.topic}: {e}")
            return result
            
    def __init__(self, topic: str, *,
                 host: str="localhost",
                 port: int=1883,
                 credentials: TLSCredentials | None=None,
                 formatter: Formatter | None=None,
                 **kwargs):
                #  connection: Connection | None=None, formatter: Formatter | None=None, **kwargs):
        self.connection = Connection(host, port, credentials=credentials, **kwargs)                
        # self.connection: Connection = connection or Connection()
        self.topic: str = topic
        self.kwargs = kwargs
        self.formatter = formatter or Formatter()

    def __enter__(self) -> SyncClient:
        logger.debug("Entering Publisher context.")
        client = self.connection.__enter__()
        logger.debug("Publisher context setup complete.")
        return client

    def __exit__(self, *exc):
        self.connection.__exit__()
        logger.debug("Exited Publisher context.")

    async def __aenter__(self) -> AsyncClient:
        logger.debug("Entering async Publisher context.")
        client = await self.connection.__aenter__()
        logger.debug("Async Publisher context setup complete.")
        return client

    async def __aexit__(self, *exc):
        await self.connection.__aexit__(*exc)
        logger.debug("Exited async Publisher context.")

    def __call__(self, fn):
        if isinstance(fn, Publisher.Task):
            logger.debug(f"Wrapping Task function '{fn.fn.__name__}'.")
            return type(fn)(self, fn.__call__)
        if inspect.iscoroutinefunction(fn):
            logger.debug(f"Wrapping coroutine function '{fn.__name__}'.")
            return Publisher.AsyncTask(self, fn)
        else:
            logger.debug(f"Wrapping function '{fn.__name__}'.")
            return Publisher.SyncTask(self, fn)

publish = Publisher
