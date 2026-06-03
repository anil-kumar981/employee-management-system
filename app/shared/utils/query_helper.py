from typing import Type, TypeVar, Dict, Any, Tuple, List, Optional
from sqlalchemy import select, func, or_, cast, String, desc, asc
from sqlalchemy.sql import Select
from datetime import datetime, date

T = TypeVar("T")


def apply_query_params(
    stmt: Select,
    model: Type[T],
    params: Dict[str, Any],
    searchable_columns: Optional[List[str]] = None,
    column_aliases: Optional[Dict[str, str]] = None,
    sortable_columns: Optional[List[str]] = None,
) -> Tuple[Select, Select, Dict[str, Any]]:
    """
    Applies search, filtering, multi-field sorting, and pagination to a SQLAlchemy statement.

    Args:
        stmt: The base SQLAlchemy select statement.
        model: The SQLAlchemy model class.
        params: Dictionary of query parameters (usually request.args).
        searchable_columns: Columns searched during a global 'search' query.
        column_aliases: Dict mapping API query keys to DB model column names (e.g. designation -> department).
        sortable_columns: Allowed columns for sorting. If None, all model columns are sortable.

    Returns:
        A tuple of (paginated_stmt, count_stmt, meta_info)
        where meta_info dict contains the page and limit.
    """
    filtered_stmt = stmt
    aliases = column_aliases or {}

    # 1. Parsing Pagination parameters
    try:
        page = int(params.get("page", 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    try:
        limit = int(params.get("limit", 10))
        if limit < 1:
            limit = 10
    except (ValueError, TypeError):
        limit = 10

    # 2. Global Text Search
    search_query = params.get("search")
    if search_query and searchable_columns:
        search_query = search_query.strip()
        search_filters = []
        for col_name in searchable_columns:
            db_col_name = aliases.get(col_name, col_name)
            if hasattr(model, db_col_name):
                col = getattr(model, db_col_name)
                # Check column python type for casting
                try:
                    python_type = col.type.python_type
                except Exception:
                    python_type = str

                if python_type in (date, datetime, int, float):
                    search_filters.append(cast(col, String).ilike(f"%{search_query}%"))
                else:
                    search_filters.append(col.ilike(f"%{search_query}%"))

        if search_filters:
            filtered_stmt = filtered_stmt.filter(or_(*search_filters))

    # 3. Individual Field Filtering
    for param_name, value in params.items():
        if param_name in ("page", "limit", "sort", "search"):
            continue

        if value is None or (isinstance(value, str) and not value.strip()):
            continue

        db_col_name = aliases.get(param_name, param_name)
        if hasattr(model, db_col_name):
            col = getattr(model, db_col_name)
            try:
                python_type = col.type.python_type
            except Exception:
                python_type = str

            if python_type in (date, datetime):
                # Attempt to parse date from string
                try:
                    if isinstance(value, str):
                        parsed_date = datetime.strptime(
                            value.strip(), "%Y-%m-%d"
                        ).date()
                    else:
                        parsed_date = value
                    filtered_stmt = filtered_stmt.filter(col == parsed_date)
                except ValueError:
                    # Ignore invalid date values instead of crashing
                    pass
            elif python_type in (int, float):
                try:
                    filtered_stmt = filtered_stmt.filter(col == python_type(value))
                except ValueError:
                    # Ignore invalid numeric values instead of crashing
                    pass
            else:
                filtered_stmt = filtered_stmt.filter(col.ilike(f"%{value}%"))

    # Construct count query (without sorting and pagination)
    count_stmt = select(func.count()).select_from(filtered_stmt.subquery())

    # 4. Sorting
    sort_query = params.get("sort")
    sort_clauses = []

    if sort_query:
        # Split on commas to support multi-field sorting
        parts = sort_query.split(",")
        for part in parts:
            part = part.strip()
            if not part:
                continue

            # Handle field:order format (e.g. name:asc) or -field format (e.g. -name)
            if ":" in part:
                field, order = part.split(":", 1)
                field = field.strip()
                order = order.strip().lower()
            elif part.startswith("-"):
                field = part[1:].strip()
                order = "desc"
            else:
                field = part
                order = "asc"

            db_col_name = aliases.get(field, field)

            # Verify if field is allowed to be sorted
            if (
                sortable_columns
                and field not in sortable_columns
                and db_col_name not in sortable_columns
            ):
                continue
            if not hasattr(model, db_col_name):
                continue

            col = getattr(model, db_col_name)
            if order == "desc":
                sort_clauses.append(desc(col))
            else:
                sort_clauses.append(asc(col))

    # Fallback to default sorting (id ASC) if no sort clause applied
    if not sort_clauses:
        if hasattr(model, "id"):
            sort_clauses.append(asc(model.id))

    filtered_stmt = filtered_stmt.order_by(*sort_clauses)

    # 5. Pagination Offset/Limit
    offset = (page - 1) * limit
    paginated_stmt = filtered_stmt.offset(offset).limit(limit)

    meta_info = {"page": page, "limit": limit}

    return paginated_stmt, count_stmt, meta_info
