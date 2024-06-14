import logging
import time
from fastapi import Request

log = logging.getLogger("api")


async def access_log(request: Request, call_next):
    t0 = time.time()
    resp = await call_next(request)
    log.info("%s %s -> %d (%dms)", request.method, request.url.path, resp.status_code, (time.time() - t0) * 1000)
    return resp
