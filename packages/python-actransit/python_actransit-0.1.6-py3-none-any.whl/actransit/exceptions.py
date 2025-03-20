class BadResponse(Exception):
    """Bad or malformatted response content."""


class HTTPError(Exception):
    """Invalid HTTP response or loss of request connection."""
