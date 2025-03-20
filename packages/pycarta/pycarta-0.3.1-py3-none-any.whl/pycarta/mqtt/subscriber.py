import os
import asyncio
import inspect
import logging
import threading
from aiomqtt import MqttError, MqttCodeError
from queue import Queue
from .client import AsyncClient, SyncClient
from .connection import Connection
from .credentials import TLSCredentials
from .formatter import Formatter

logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())


class Subscriber:
    class Task:
        def __init__(self, scope: "Subscriber", function: callable, *, timeout: float=10.0):
            self.scope = scope
            self.fn = function
            self.timeout: float = timeout
            self._lock: asyncio.Lock = asyncio.Lock()

    class AsyncTask(Task):
        def __init__(self, *args, **kwds):
            super().__init__(*args, **kwds)
            self.client = None

        def __aiter__(self):
            return self

        async def __anext__(self):
            # Context is reentrant.
            client = await self.__aenter__()
            # await client.subscribe(self.scope.topic, **self.scope.kwargs)
            try:
                try:
                    message = await anext(client.messages)
                except asyncio.CancelledError:
                    logger.debug("Future or Task was cancelled.")
                    raise StopAsyncIteration()
                except KeyboardInterrupt:
                    logger.debug("Iteration halted with Keyboard Interrupt.")
                    raise StopAsyncIteration()
                except (MqttError, MqttCodeError) as e:
                    logger.info("Disconnected from the broker. Waiting to reconnect.")
                    # raise StopAsyncIteration()
                    # async with self._lock:
                    await self.__aexit__(type(e), e, None)
                    client = await self.__aenter__()
                    logger.info("Reconnected to the broker.")
                    return await anext(self)
                except Exception as e:
                    logger.debug(f"An unknown error occured: {e}")
                else:
                    return await self.fn(self.scope.formatter.unpack(message.payload))
            except Exception as e:
                await self.__aexit__(type(e), e, None)
                raise e

        async def __aenter__(self) -> AsyncClient:
            async with self._lock:
                self.client = await self.scope.__aenter__()
                await self.client.subscribe(**self.scope.kwargs)
                logger.debug("Async Task context setup complete.")
            return self.client

        async def __aexit__(self, *exc):
            async with self._lock:
                if self.client:
                    logger.debug("Tearing down async Task context.")
                    await self.scope.__aexit__(*exc)
                    # self.client = None
                    logger.debug("Exited async Task context.")

        async def __call__(self):
            rval = await anext(self)
            # Stop listening.
            await self.__aexit__(None, None, None)
            return rval
            
    class SyncTask(Task):
        def __init__(self, *args, **kwds):
            super().__init__(*args, **kwds)
            self.scope.connection.callbacks["on_connect"] = self.on_connect
            self.scope.connection.callbacks["on_message"] = self.on_message
            self.client = None
            self.queue: Queue = Queue()
            self._lock: threading.Lock = threading.Lock()

        def __iter__(self):
            return self

        def __next__(self):
            if not self.client:
                client = self.__enter__()
            try:
                return self.queue.get()
            except KeyboardInterrupt:
                logger.debug("Keyboard interrupt stopped Subscriber iteration.")
                raise StopIteration()
            except TimeoutError:
                logger.debug("A timeout interrupted Subscriber iteration.")
                raise StopIteration()
            except Exception as e:
                logger.error(f"An unexpected exception occured during Subscriber iteration: {e}.")
                self.__exit__(type(e), e, None)
                self.__enter__()
                return next(self)

        def __enter__(self):
            # Context is reentrant
            with self._lock:
                if self.client is None:
                    logger.debug("Entering Subscriber task context.")
                    self.client = self.scope.__enter__()
            logger.debug("Subscriber task context setup complete.")
            return self.client

        def __exit__(self, *exc):
            with self._lock:
                if self.client:
                    logger.debug("Tearing down Subscriber task context.")
                    self.scope.__exit__(*exc)
                    self.client = None
            logger.debug("Exited Subscriber task context.")

        def __call__(self):
            logger.debug("Called Subscriber.Task.__call__")
            rval =  next(self)
            # Stop listening.
            self.__exit__(None, None, None)
            return rval

        def on_message(self, client, userdata, message):
            logger.debug("Calling Subscriber.Task.on_message callback.")
            result = self.fn(self.scope.formatter.unpack(message.payload))
            self.queue.put(result)

        def on_connect(self, client, userdata, connect_flags, reason_code, properties):
            logger.debug("Calling Subscriber.Task.on_connect callback.")
            self.scope.connection.on_connect(client, userdata, connect_flags, reason_code, properties)
            client.subscribe(**self.scope.kwargs)
            
    def __init__(self, topic: str, host: str="localhost", port: int=1883,
                 *,
                 credentials: TLSCredentials | None=None,
                 qos: int=0,
                 options=None,
                 properties=None,
                #  connection: Connection | None=None,
                 formatter: Formatter | None=None,
                 **kwargs):
        self.connection = Connection(host, port, credentials=credentials, **kwargs)
        # self.connection: Connection = connection or Connection(**kwargs)
        self.kwargs = {
            "topic": topic,
            "qos": qos,
            "options": options,
            "properties": properties
        }
        self.formatter = formatter or Formatter()

    def __enter__(self) -> SyncClient:
        logger.debug("Entering Subscriber context.")
        client = self.connection.__enter__()
        logger.debug("Subscriber context setup complete.")
        return client

    def __exit__(self, *exc):
        self.connection.__exit__()
        logger.debug("Exited Subscriber context.")

    async def __aenter__(self) -> AsyncClient:
        logger.debug("Entering async Subscriber context.")
        client = await self.connection.__aenter__()
        logger.debug("Async Subscriber context setup complete.")
        return client

    async def __aexit__(self, *exc):
        await self.connection.__aexit__(*exc)
        logger.debug("Exited async Subscriber context.")

    def __call__(self, fn):
        if isinstance(fn, Subscriber.Task):
            msg = """
pycarta.mqtt does not currently support multiple (stacked) decorators.
Please consider refactoring as follows:

def my_func(msg):
    pass
    
sub1 = subscribe(topic1, host1, port1, ...)(my_func)
sub2 = subscribe(topic2, host2, port2,...)(my_func)
"""
            raise NotImplementedError(msg)
        elif inspect.iscoroutinefunction(fn):
            logger.debug(f"Wrapping coroutine function '{fn.__name__}'.")
            return Subscriber.AsyncTask(self, fn)
        else:
            logger.debug(f"Wrapping function '{fn.__name__}'.")
            return Subscriber.SyncTask(self, fn)

subscribe = Subscriber
