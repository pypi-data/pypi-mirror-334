import random
import socket
import logging
from typing import Optional
from functools import lru_cache

from ._connection_base import Connection
from ... import defaults

logger = logging.getLogger(__name__)


class TcpConnection(Connection):
    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        min_port: Optional[int] = None,
        num_ports: Optional[int] = None,
    ) -> None:
        if host is None:
            host = get_host()
        if port is None:
            self._server_sock = lock_port(host, min_port=min_port, num_ports=num_ports)
        else:
            self._server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._server_sock.bind((host, port))
        port = self._server_sock.getsockname()[-1]

        self._host = host
        self._port = port
        self._hostport = f"{host}:{port}"

        self._client_socket = None

        self._server_sock.listen(1)
        self._server_sock.settimeout(0.5)

        logger.debug("start listening on %s:%s", host, port)
        super().__init__()

    @property
    def input_name(self) -> str:
        return self._hostport

    @property
    def output_name(self) -> str:
        return self._hostport

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> str:
        return self._port

    def close(self):
        if self._client_socket:
            self._client_socket.close()
        self._server_sock.close()

    def wait_client(self) -> None:
        if self._client_socket is not None:
            return
        with self._wait_client_context() as it:
            for _ in it:
                try:
                    self._client_socket, _ = self._server_sock.accept()
                    break
                except socket.timeout:
                    pass

    def receive_nbytes(self, nbytes: int) -> bytes:
        buffer = None
        with self._receive_nbytes_context(nbytes) as it:
            for buffer in it:
                if self._client_socket is None:
                    self.wait_client()
                buffer.data += self._client_socket.recv(buffer.chunk_size)
        if buffer is None:
            raise RuntimeError(f"did not receive data from {self.input_name}")
        return buffer.data

    def send_bytes(self, data: bytes) -> None:
        if self.cancelled():
            raise RuntimeError(f"send to {self.output_name} is cancelled")
        if self._client_socket is None:
            self.wait_client()
        self._client_socket.sendall(data)


@lru_cache(1)
def get_host() -> str:
    return socket.gethostbyname(socket.gethostname())


def lock_port(
    host: str, min_port: Optional[int] = None, num_ports: Optional[int] = None
) -> int:
    if min_port is None:
        min_port = defaults.MIN_PORT
    if num_ports is None:
        num_ports = defaults.NUM_PORTS
    preferred_ports = list(range(min_port, min_port + num_ports + 1))
    random.shuffle(preferred_ports)

    # Find a free port in the preferred range
    for port in preferred_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((host, port))
            return sock
        except Exception:
            sock.close()
        except BaseException:
            sock.close()
            raise

    # Preferred ports are already in use, find any free port.
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind((host, 0))
            return sock
        except Exception:
            sock.close()
        except BaseException:
            sock.close()
            raise
