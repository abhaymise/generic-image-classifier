from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse


class LimitRequestSizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        max_size = 100 * 1024 * 1024  # 100 MB
        endpoint = request.url.path
        # print(endpoint)
        if endpoint  in ["/","/health"]:
            return await call_next(request)
        content_length = request.headers.get("content-length")
        print(f"received file of size {content_length} bytes")
        if content_length and int(content_length) > max_size:
            return JSONResponse(content={"detail": "File size exceeds limit"}, status_code=413)
        return await call_next(request)