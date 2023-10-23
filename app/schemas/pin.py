from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class Pin(BaseModel):
    key: str
    attribute: str
    value: Optional[str] = None
