import os
import time
import logging
import warnings
from uuid import uuid4

from ._connection_base import Connection
from ... import os_utils

logger = logging.getLogger(__name__)


class FileConnection(Connection):
    def __init__(self, directory: str, basename: str) -> None:
        conn_id = str(uuid4())
        os_utils.makedirs(directory)
        input_filename = os.path.join(directory, f"{basename}.in.{conn_id}.pkl")
        output_filename = os.path.join(directory, f"{basename}.out.{conn_id}.pkl")

        self._input_filename = input_filename
        self._output_filename = output_filename
        self._output_file = None
        self._input_file = open(input_filename, "wb+")

        logger.debug("start writing %s", input_filename)
        super().__init__()

    @property
    def input_name(self) -> str:
        return self._output_filename

    @property
    def output_name(self) -> str:
        return self._input_filename

    @property
    def input_filename(self) -> str:
        return self._input_filename

    @property
    def output_filename(self) -> str:
        return self._output_filename

    def close(self):
        if self._input_file is not None:
            self._input_file.close()
            self._input_file = None
            _delete_file_with_retry(self._input_filename)
        if self._output_file is not None:
            self._output_file.close()
            self._output_file = None
            _delete_file_with_retry(self._output_filename)

    def wait_client(self) -> None:
        if self._output_file is not None:
            return
        with self._wait_client_context() as it:
            dirname = os.path.dirname(self._output_filename)
            for _ in it:
                try:
                    _ = os.listdir(dirname)  # force NFS cache
                    self._output_file = open(self._output_filename, "rb+")
                    break
                except FileNotFoundError:
                    continue

    def receive_nbytes(self, nbytes: int) -> bytes:
        buffer = None
        with self._receive_nbytes_context(nbytes) as it:
            for buffer in it:
                if self._output_file is None:
                    self.wait_client()
                buffer.data += self._output_file.read(buffer.chunk_size)
        if buffer is None:
            raise RuntimeError(f"did not receive data from {self}")
        return buffer.data

    def send_bytes(self, data: bytes) -> None:
        if self.cancelled():
            raise RuntimeError(f"send to %{self} is cancelled")
        self._input_file.write(data)
        self._input_file.flush()


def _delete_file_with_retry(
    filename: str,
    max_attempts: int = 5,
    initial_delay: float = 0.1,
    max_delay: float = 1,
) -> None:
    delay = initial_delay / 2
    for _ in range(max_attempts):
        try:
            os.remove(filename)
            return
        except PermissionError:
            delay = min(delay * 2, max_delay)
            time.sleep(delay)
    warnings.warn(f"Could not remove file {filename}", UserWarning, stacklevel=2)
