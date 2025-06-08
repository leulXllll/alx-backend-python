#!/usr/bin/env python3
"""Authentication utilities for the chats module."""

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from django.contrib.auth.models import User
from typing import Optional, Tuple, Any


class CustomJWTAuthentication(JWTAuthentication):
    """Custom JWT authentication to validate tokens and retrieve users."""

    def authenticate(self, request: Any) -> Optional[Tuple[User, Any]]:
        """Authenticate the request using JWT and return user and token."""
        try:
            user, validated_token = super().authenticate(request)
            return user, validated_token
        except InvalidToken:
            return None