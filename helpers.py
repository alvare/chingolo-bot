from functools import wraps
import aiohttp

async def async_get(url, **kwargs):
    async with aiohttp.ClientSession(raise_for_status=True,
                                     conn_timeout=30,
                                     read_timeout=30) as session:
        async with session.get(url, **kwargs) as resp:
            return await resp.json()

markdown_escapes = str.maketrans({
    "`":  r"\`",
    "*":  r"\*",
    "_":  r"\_",
    "[":  r"\["})

def command(docstring):
    def wrapped(fn):
        @wraps(fn)
        def wrapped_f(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapped_f.docstring = docstring
        return wrapped_f
    return wrapped
