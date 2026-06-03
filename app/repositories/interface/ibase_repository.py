from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional, Union, Tuple, Dict, Any

T = TypeVar("T")


class IBaseRepo(ABC, Generic[T]):
    """Generic base interface declaring standard database CRUD operations."""

    @abstractmethod
    async def add(self, entity: T) -> T:
        """Add a new entity record."""
        pass

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """Fetch a record by its unique identifier."""
        pass

    @abstractmethod
    async def get_all(
        self, params: Optional[Dict[str, Any]] = None
    ) -> Union[List[T], Tuple[List[T], Dict[str, Any]]]:
        """Fetch all records."""
        pass

    @abstractmethod
    async def update(self, entity: T) -> T:
        """Apply structural updates to an existing record."""
        pass

    @abstractmethod
    async def delete(self, entity_id: int) -> bool:
        """Remove a record by its unique identifier."""
        pass
