# backend/core/__init__.py
"""
Core modules for configuration, database, and schemas
"""
from core.config import settings
from core.database import db
from core.schemas import *

__all__ = ['settings', 'db']

