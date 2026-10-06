"""URL safety guard for the MCP check server."""

import ipaddress
import socket
from urllib.parse import urlparse


def is_public_url(url: str) -> bool:
    """Return True only for HTTPS URLs that resolve to public IP addresses."""
    try:
        parsed = urlparse(url)

        if parsed.scheme != "https" or not parsed.hostname:
            return False

        host = parsed.hostname

        try:
            ip = ipaddress.ip_address(host)
            return ip.is_global
        except ValueError:
            pass

        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        if not addresses:
            return False

        return all(ipaddress.ip_address(addr[4][0]).is_global for addr in addresses)
    except (OSError, ValueError):
        return False