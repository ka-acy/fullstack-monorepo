from fastapi import Header, HTTPException

from app.auth import TokenVerificationError, verify_bearer_token


def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.removeprefix("Bearer ").strip()

    try:
        return verify_bearer_token(token)
    except TokenVerificationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail) from e
    except Exception:
        raise HTTPException(status_code=500, detail="Token verification unavailable")
