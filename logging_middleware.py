import time
import logging
from fastapi import Request

logger = logging.getLogger("uvicorn.access")

async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # Log the request
    logger.info(f"📥 {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Log response time
    process_time = time.time() - start_time
    logger.info(f"📤 {request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response
