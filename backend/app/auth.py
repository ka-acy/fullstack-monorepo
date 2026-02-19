import os
from functools import lru_cache
from typing import Any

import requests
from jose import jwt
from jose.exceptions import JWTError


class TokenVerificationError(Exception):
    def __init__(self, detail: str, status_code: int = 401):
        super().__init__(detail)
        self.detail = detail
        self.status_code = status_code


def _env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"{name} is not set")
    return val


def _issuer() -> str:
    configured_issuer = os.getenv("SUPABASE_JWT_ISSUER")
    if configured_issuer:
        return configured_issuer

    # Fallback for local dev based on standard Supabase JWKS path.
    jwks_url = _env("SUPABASE_JWKS_URL")
    suffix = "/.well-known/jwks.json"
    if jwks_url.endswith(suffix):
        return jwks_url[: -len(suffix)]

    raise RuntimeError(
        "SUPABASE_JWT_ISSUER is not set and could not be inferred from SUPABASE_JWKS_URL"
    )


@lru_cache(maxsize=1)
def _jwks() -> dict[str, Any]:
    url = _env("SUPABASE_JWKS_URL")
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()


def _pick_signing_key(jwks: dict[str, Any], kid: str) -> dict[str, Any] | None:
    keys = jwks.get("keys", [])
    return next((k for k in keys if k.get("kid") == kid), None)


def verify_bearer_token(token: str) -> dict[str, Any]:
    audience = os.getenv("SUPABASE_JWT_AUDIENCE", "authenticated")
    issuer = _issuer()

    try:
        header = jwt.get_unverified_header(token)
    except JWTError as e:
        raise TokenVerificationError("Invalid token header") from e

    kid = header.get("kid")
    if not kid:
        raise TokenVerificationError("Token missing key id")

    algorithm = header.get("alg", "RS256")
    if algorithm not in {"RS256", "ES256"}:
        raise TokenVerificationError("Unsupported token algorithm")

    try:
        jwks = _jwks()
    except (requests.RequestException, RuntimeError) as e:
        raise TokenVerificationError(
            "Unable to load token signing keys",
            status_code=503,
        ) from e

    key = _pick_signing_key(jwks, kid)

    # Signing keys can rotate; refresh cache once before failing.
    if not key:
        _jwks.cache_clear()
        try:
            key = _pick_signing_key(_jwks(), kid)
        except (requests.RequestException, RuntimeError) as e:
            raise TokenVerificationError(
                "Unable to refresh token signing keys",
                status_code=503,
            ) from e

    if not key:
        raise TokenVerificationError("Signing key not found for token")

    try:
        return jwt.decode(
            token,
            key,
            algorithms=[algorithm],
            audience=audience,
            issuer=issuer,
            options={"verify_iss": True},
        )
    except JWTError as e:
        raise TokenVerificationError("Invalid or expired token") from e
