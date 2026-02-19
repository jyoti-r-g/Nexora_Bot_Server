from src.config.index import appConfig
from fastapi import Request, HTTPException

from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions




# Initialize SDK globally to allow internal caching (e.g. JWKS)
clerk_sdk = Clerk(bearer_auth=appConfig["clerk_secret_key"])

# Simple in-memory cache: token -> (clerk_id, timestamp)
token_cache = {}
CACHE_TTL = 60  # Cache duration in seconds

import time

def get_current_user_clerk_id(request: Request):
    start = time.time()
    try:
        # Check cache first
        auth_header = request.headers.get("Authorization")
        
        with open("auth_debug.log", "a") as f:
            f.write(f"DEBUG: Auth Header present: {bool(auth_header)}\n")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            if token in token_cache:
                cached_clerk_id, timestamp = token_cache[token]
                if time.time() - timestamp < CACHE_TTL:
                    print(f"[Profiling] Cache hit! Took: {time.time() - start}s")
                    return cached_clerk_id
                else:
                    del token_cache[token] # Expired

        # request_state = JWT Token
        request_state = clerk_sdk.authenticate_request(
            request,
            options=AuthenticateRequestOptions(authorized_parties=appConfig["domain"]),
        )

        if not request_state.is_signed_in:
            raise HTTPException(status_code=401, detail="User is not signed in")

        clerk_id = request_state.payload.get("sub")

        if not clerk_id:
            raise HTTPException(status_code=401, detail="Clerk ID not found in token")

        # Update cache
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            token_cache[token] = (clerk_id, time.time())

        end = time.time()
        print(f"[Profiling] Clerk Auth (Miss) took: {end - start}s")
        with open("auth_debug.log", "a") as f:
             f.write(f"DEBUG: Auth Success. Clerk ID: {clerk_id}\n")
        return clerk_id

    except HTTPException as e:
        with open("auth_debug.log", "a") as f:
             f.write(f"DEBUG: Auth HTTPException: {e.detail}\n")
        raise e

    except Exception as e:
        # Check for "HTTPException-like" objects (duck typing)
        # This handles cases where the exception class might verify as different 
        # due to reloading or different import paths, but strictly has the same structure.
        if hasattr(e, "status_code") and hasattr(e, "detail"):
             raise HTTPException(
                status_code=e.status_code,
                detail=e.detail
            )
            
        print(f"Clerk Auth Error: {str(e)}")
        with open("auth_debug.log", "a") as f:
             f.write(f"DEBUG: Clerk Auth Error: {str(e)}\n")
        raise HTTPException(
            status_code=500,
            detail=f"Clerk SDK Failed. {str(e)}",
        )
