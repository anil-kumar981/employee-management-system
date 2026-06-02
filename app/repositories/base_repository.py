from typing import Type, TypeVar, List, Optional
from sqlalchemy import select
from app.repositories.interface.ibase_repository import IBaseRepo
from app.database.database import get_db

T = TypeVar("T")

class BaseRepo(IBaseRepo[T]):
    """Generic concrete database repository implementing standard CRUD natively using SQLAlchemy sessions."""
    
    def __init__(self, model: Type[T], get_db=get_db) -> None:
        self.model = model
        self.get_db = get_db
        
    async def add(self, entity: T) -> T:
        """Add a new entity record dynamically to the database."""
        async with self.get_db() as session:
            try:
                session.add(entity)
                await session.commit()
                await session.refresh(entity)
                return entity
            except Exception as e:
                await session.rollback()
                raise e
            
    async def get_by_id(self, entity_id: int) -> Optional[T]:
        """Fetch a record by its unique identifier."""
        async with self.get_db() as session:
            return await session.get(self.model, entity_id)
            
    async def get_all(self) -> List[T]:
        """Fetch all records."""
        async with self.get_db() as session:
            result = await session.execute(select(self.model))
            return list(result.scalars().all())
            
    async def update(self, entity: T) -> T:
        """Apply structural updates to an existing record."""
        async with self.get_db() as session:
            try:
                merged = await session.merge(entity)
                await session.commit()
                await session.refresh(merged)
                return merged
            except Exception as e:
                await session.rollback()
                raise e
            
    async def delete(self, entity_id: int) -> bool:
        """Remove a record by its unique identifier."""
        async with self.get_db() as session:
            try:
                entity = await session.get(self.model, entity_id)
                if entity:
                    await session.delete(entity)
                    await session.commit()
                    return True
                return False
            except Exception as e:
                await session.rollback()
                raise e
