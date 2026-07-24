import re

_YOUTUBE_PATTERNS = [
    r"(?:youtube\.com/watch\?v=|youtube\.com/embed/|youtube\.com/shorts/|youtu\.be/)([A-Za-z0-9_-]{11})",
]


def extract_youtube_id(url):
    """Pull an 11-char YouTube video ID out of common URL shapes.

    Returns None if the URL doesn't look like a YouTube link -- callers
    should never fall back to rendering the raw URL in an iframe.
    """
    if not url:
        return None
    for pattern in _YOUTUBE_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
