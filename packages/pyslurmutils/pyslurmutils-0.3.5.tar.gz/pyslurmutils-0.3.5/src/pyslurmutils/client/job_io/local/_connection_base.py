import abc
import time
import pickle
import logging
import threading
from contextlib import contextmanager
from typing import Generator, Tuple, Any, Optional, Iterator


logger = logging.getLogger(__name__)


class Connection(abc.ABC):
    _HEADER_NBYTES = 4

    def __init__(self) -> None:
        self._cancel_event = threading.Event()
        self._yield_period = 1

    @property
    @abc.abstractmethod
    def input_name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def output_name(self) -> str:
        pass

    def __enter__(self) -> "Connection":
        return self

    def __exit__(self, *_) -> None:
        self.close()

    def cancel(self) -> None:
        self._cancel_event.set()

    def cancelled(self) -> bool:
        return self._cancel_event.is_set()

    @abc.abstractmethod
    def close(self):
        pass

    @abc.abstractmethod
    def wait_client(self) -> None:
        """Wait for the client to be online"""
        pass

    @contextmanager
    def _wait_client_context(self) -> Generator[None, None, None]:
        logger.debug("waiting for remote job to connect to %s ...", self.output_name)
        try:
            yield self._wait_client_iterator()
        except Exception:
            logger.debug(
                "waiting for remote job to connect to %s failed", self.output_name
            )
            raise
        if self.cancelled():
            logger.debug(
                "waiting for remote job to connect to %s cancelled", self.output_name
            )
        else:
            logger.debug("remote job connected to %s", self.output_name)

    def _wait_client_iterator(self) -> Iterator[None]:
        while not self.cancelled():
            yield
            time.sleep(self._yield_period)

    @abc.abstractmethod
    def receive_nbytes(self, nbytes: int) -> bytes:
        pass

    @contextmanager
    def _receive_nbytes_context(self, nbytes: int) -> Generator[None, None, None]:
        buffer = _Buffer(nbytes)

        yield self._receive_nbytes_iterator(buffer, nbytes)

        if len(buffer.data) != nbytes:
            err_msg = f"{len(buffer.data)} bytes received from {self.input_name} instead of {nbytes} bytes"
            if self.cancelled():
                raise ValueError(f"{err_msg} (cancelled)")
            else:
                raise ValueError(err_msg)

    def _receive_nbytes_iterator(
        self, buffer: "_Buffer", nbytes: int
    ) -> Iterator["_Buffer"]:
        while not self.cancelled() and len(buffer.data) < nbytes:
            yield buffer
            time.sleep(self._yield_period)

    @abc.abstractmethod
    def send_bytes(self, data: bytes) -> None:
        pass

    def send_data(self, data: Any) -> None:
        bdata = self._serialize_data(data)
        nbytes = len(bdata)
        logger.debug(
            "send data %s (%d bytes) to client of %s ...",
            type(data),
            nbytes,
            self.output_name,
        )
        bheader = self._serialize_header(bdata)
        try:
            self.send_bytes(bheader + bdata)
        except (BrokenPipeError, ConnectionResetError):
            if data is None:
                logger.debug("client of %s already exited", self.output_name)
                return
            raise
        logger.debug("data send to client of %s", self.output_name)

    def receive_data(self) -> Tuple[Any, Optional[BaseException]]:
        logger.debug("waiting for client data on %s ...", self.input_name)
        bheader = self.receive_nbytes(self._HEADER_NBYTES)
        nbytes = self._deserialize_header(bheader)
        if nbytes:
            logger.debug(
                "receiving %d bytes from client on %s ...", nbytes, self.input_name
            )
        else:
            logger.warning(
                "receiving %d bytes from client on %s (corrupt data?) ...",
                nbytes,
                self.input_name,
            )
        bdata = self.receive_nbytes(nbytes)
        logger.debug("client data received from %s", self.input_name)
        return self._deserialize_data(bdata)

    def _serialize_header(self, bdata: bytes) -> bytes:
        return len(bdata).to_bytes(self._HEADER_NBYTES, "big")

    def _deserialize_header(self, bheader: bytes) -> int:
        return int.from_bytes(bheader, "big")

    def _serialize_data(self, data: Any) -> bytes:
        return pickle.dumps(data)

    def _deserialize_data(self, data: bytes) -> Any:
        return pickle.loads(data)


class _Buffer:
    def __init__(self, nbytes: int) -> None:
        self.data = b""
        self._nbytes = nbytes
        self._max_chunk_size = min(nbytes, 512)

    @property
    def chunk_size(self) -> int:
        return min(self._max_chunk_size, self._nbytes - len(self.data))
