import time
from fastapi import Request, HTTPException


_HITS: dict[str, list[float]] = {}


def rate_limit(max_per_minute: int = 60):
    async def dep(request: Request):
        ip = request.client.host if request.client else "unknown"
        now = time.time()
        arr = [t for t in _HITS.get(ip, []) if now - t < 60]
        arr.append(now)
        _HITS[ip] = arr
        if len(arr) > max_per_minute:
            raise HTTPException(429, "too many requests")
    return dep
