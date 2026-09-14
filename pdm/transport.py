"""Tiny TCP transport used to measure a real producer/consumer boundary."""

import socket
import struct


def send_frame(host: str, port: int, payload: bytes) -> int:
    """Send one length-prefixed frame and return payload bytes sent."""
    with socket.create_connection((host, port), timeout=10) as sock:
        sock.sendall(struct.pack("!Q", len(payload)))
        sock.sendall(payload)
        return len(payload)


def receive_frame(connection: socket.socket) -> bytes:
    """Receive one length-prefixed frame."""
    header = _recv_exact(connection, 8)
    size = struct.unpack("!Q", header)[0]
    if size > 256 * 1024 * 1024:
        raise ValueError("frame is too large")
    return _recv_exact(connection, size)


def _recv_exact(connection: socket.socket, size: int) -> bytes:
    chunks = []
    remaining = size
    while remaining:
        chunk = connection.recv(min(remaining, 64 * 1024))
        if not chunk:
            raise ConnectionError("connection closed before frame completed")
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)
