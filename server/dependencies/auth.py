from fastapi import HTTPException, Request
from firebase_admin import auth


def firebase_auth_dependency(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid Authorization header"
        )

    token = auth_header.split(" ")[1]

    try:
        decoded_token = auth.verify_id_token(token)
        user_id = decoded_token.get("uid")

        user_record = auth.get_user(user_id)

        return user_record
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")
