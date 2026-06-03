from typing import Type, TypeVar, List, Optional, Union, Tuple, Dict, Any
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
            
    async def get_all(self, params: Optional[Dict[str, Any]] = None) -> Union[List[T], Tuple[List[T], Dict[str, Any]]]:
        """Fetch all records, optionally applying pagination, sorting, and searching."""
        async with self.get_db() as session:
            if params is None:
                result = await session.execute(select(self.model))
                return list(result.scalars().all())
                
            from app.shared.utils.query_helper import apply_query_params
            import math
            
            searchable_columns = getattr(self, "SEARCHABLE_COLUMNS", None)
            column_aliases = getattr(self, "COLUMN_ALIASES", None)
            sortable_columns = getattr(self, "SORTABLE_COLUMNS", None)
            
            if searchable_columns is None:
                from sqlalchemy import String
                searchable_columns = [
                    c.key for c in self.model.__table__.columns 
                    if isinstance(c.type, String)
                ]
                
            paginated_stmt, count_stmt, meta_info = apply_query_params(
                stmt=select(self.model),
                model=self.model,
                params=params,
                searchable_columns=searchable_columns,
                column_aliases=column_aliases,
                sortable_columns=sortable_columns
            )
            
            # Execute count query
            count_result = await session.execute(count_stmt)
            total_results = count_result.scalar_one()
            
            # Execute paginated items query
            result = await session.execute(paginated_stmt)
            items = list(result.scalars().all())
            
            page = meta_info["page"]
            limit = meta_info["limit"]
            total_pages = math.ceil(total_results / limit) if limit > 0 else 0
            
            pagination_meta = {
                "page": page,
                "limit": limit,
                "total_results": total_results,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1
            }
            
            return items, pagination_meta
            
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
