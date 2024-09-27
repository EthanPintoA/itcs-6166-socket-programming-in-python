SERVER_HOST = "127.0.0.1"  # Loopback address or localhost
SERVER_PORT = 5222  # Arbitrary port number

BUF_SIZE = 1024  # 1024 bytes or 1 KiB, arbitrary buffer size


def _addr_to_str(addr: tuple[str, int]) -> str:
    """Formats the host and port as a string."""
    host, port = addr
    return f"{host}:{port}"


def _format_msg(sender: str, msg: str) -> str:
    """Formats a message to be broadcasted."""
    sender = f"[{sender}]".ljust(15 + 6 + 2)  # 15 - IPv4, 6 - Port, 2 - Brackets
    return f"{sender} {msg}"


def connection_msg(addr: tuple[str, int]) -> str:
    """Returns a 'connection' message."""
    client = _addr_to_str(addr)
    return _format_msg("SERVER", f"'{client}' has joined the chat.")


def sent_msg(addr: tuple[str, int], msg: str) -> str:
    """Returns a 'message' message."""
    sender = _addr_to_str(addr)
    return _format_msg(sender, msg)


def disconnect_msg(addr: tuple[str, int]) -> str:
    """Returns a 'disconnect' message."""
    client = _addr_to_str(addr)
    return _format_msg("SERVER", f"'{client}' has left the chat.")
