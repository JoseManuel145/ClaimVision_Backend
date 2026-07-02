"""
Envelope de paginación estándar del contrato (sección 0 del spec):

    { "data": [...], "total": N, "page": 1, "page_size": 20 }

Usar `Page[T]` como `response_model` y `Page.build(...)` para construirlo.
"""
from typing import Generic, List, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class Page(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int
    page_size: int

    @classmethod
    def build(cls, data: List[T], total: int, page: int, page_size: int) -> "Page[T]":
        return cls(data=data, total=total, page=page, page_size=page_size)


def offset_from_page(page: int, page_size: int) -> int:
    """Traduce `page` (1-based) y `page_size` al `offset` que usan los repos."""
    return (max(page, 1) - 1) * page_size
