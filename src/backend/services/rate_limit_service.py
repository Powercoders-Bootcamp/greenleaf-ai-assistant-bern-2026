from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from threading import Lock
from time import monotonic
from typing import Deque

from fastapi import HTTPException, Request, status

from backend.core.config import (
    ADMIN_RATE_LIMIT_MAX_REQUESTS,
    ADMIN_RATE_LIMIT_WINDOW_SECONDS,
    CHAT_RATE_LIMIT_MAX_REQUESTS,
    CHAT_RATE_LIMIT_WINDOW_SECONDS,
    LOGIN_RATE_LIMIT_MAX_REQUESTS,
    LOGIN_RATE_LIMIT_WINDOW_SECONDS,
)


@dataclass(frozen=True)
class RateLimitPolicy:
    scope: str
    max_requests: int
    window_seconds: int


class InMemoryRateLimiter:
    """Small fixed-window limiter for single-process abuse protection."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._buckets: dict[str, Deque[float]] = {}

    def clear(self) -> None:
        with self._lock:
            self._buckets.clear()

    def hit(self, key: str, *, max_requests: int, window_seconds: int) -> int | None:
        now = monotonic()
        cutoff = now - window_seconds

        with self._lock:
            bucket = self._buckets.setdefault(key, deque())
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()

            if len(bucket) >= max_requests:
                return max(1, int(bucket[0] + window_seconds - now))

            bucket.append(now)

        return None


rate_limiter = InMemoryRateLimiter()

LOGIN_POLICY = RateLimitPolicy(
    scope="auth.login",
    max_requests=LOGIN_RATE_LIMIT_MAX_REQUESTS,
    window_seconds=LOGIN_RATE_LIMIT_WINDOW_SECONDS,
)
CHAT_POLICY = RateLimitPolicy(
    scope="chat.turn",
    max_requests=CHAT_RATE_LIMIT_MAX_REQUESTS,
    window_seconds=CHAT_RATE_LIMIT_WINDOW_SECONDS,
)
ADMIN_POLICY = RateLimitPolicy(
    scope="admin.route",
    max_requests=ADMIN_RATE_LIMIT_MAX_REQUESTS,
    window_seconds=ADMIN_RATE_LIMIT_WINDOW_SECONDS,
)


def _client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "").strip()
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip() or "unknown"

    if request.client and request.client.host:
        return request.client.host

    return "unknown"


def _enforce(policy: RateLimitPolicy, identity: str) -> None:
    retry_after = rate_limiter.hit(
        f"{policy.scope}:{identity}",
        max_requests=policy.max_requests,
        window_seconds=policy.window_seconds,
    )
    if retry_after is None:
        return

    raise HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail=(
            f"Rate limit exceeded for {policy.scope}. "
            f"Try again in {retry_after} seconds."
        ),
        headers={"Retry-After": str(retry_after)},
    )


def enforce_login_rate_limit(request: Request, email: str | None) -> None:
    normalized_email = (email or "").strip().lower() or "anonymous"
    identity = f"ip={_client_ip(request)}|email={normalized_email}"
    _enforce(LOGIN_POLICY, identity)


def enforce_chat_rate_limit(request: Request, user_id: int) -> None:
    identity = f"user={user_id}|ip={_client_ip(request)}"
    _enforce(CHAT_POLICY, identity)


def enforce_admin_rate_limit(request: Request, user_id: int) -> None:
    identity = f"user={user_id}|ip={_client_ip(request)}"
    _enforce(ADMIN_POLICY, identity)
