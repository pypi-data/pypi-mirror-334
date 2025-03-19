from fastapi import HTTPException, Query


VALID_API_KEYS = [
    'XX33XX'
]
"""
The API keys we accept (by now they are hardcoded).
"""

async def is_authorized_with_api_key(
    api_key: str = Query(min_length = 6, max_length = 6)
):
    # TODO: When Query fails it returns a custom
    # error, raising not this exception below
    if not api_key or api_key not in VALID_API_KEYS:
        raise HTTPException(status_code = 401, detail = 'Authorization is not valid.')

# async def is_authorized(request: Request, call_next):
#     """
#     This middleware checks if the provided query has a valid 'api_key' or not. It
#     will reject the request if not valid.
#     """
#     print(request.query_params)
#     # TODO: Change this to receive the 'api_key' as Authorization header
#     # auth = request.headers.get('Authorization')  
#     api_key = request.query_params.get('api_key')

#     # TODO: Make this read from a database of valid 'api_keys'
#     if not api_key or api_key not in VALID_API_KEYS:
#         raise HTTPException(status_code = 401, detail = 'Authorization is not valid.')

#     # TODO: Add used credits to the user related to this 'api_key'
    
#     #return await call_next(request)