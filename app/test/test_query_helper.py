from sqlalchemy import select, Integer, String, Date
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from datetime import date
from app.shared.utils.query_helper import apply_query_params

Base = declarative_base()


class DummyModel(Base):
    __tablename__ = "dummy"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    role: Mapped[str] = mapped_column(String(50))
    created_date: Mapped[date] = mapped_column(Date)


def test_apply_query_params_defaults():
    stmt = select(DummyModel)
    params = {}
    paginated, count, meta = apply_query_params(stmt, DummyModel, params)

    assert meta["page"] == 1
    assert meta["limit"] == 10
    assert paginated._limit == 10
    assert paginated._offset == 0


def test_apply_query_params_custom_pagination():
    stmt = select(DummyModel)
    params = {"page": "3", "limit": "5"}
    paginated, count, meta = apply_query_params(stmt, DummyModel, params)

    assert meta["page"] == 3
    assert meta["limit"] == 5
    assert paginated._limit == 5
    assert paginated._offset == 10


def test_apply_query_params_sorting():
    stmt = select(DummyModel)
    params = {"sort": "name:desc,email:asc"}
    paginated, count, meta = apply_query_params(
        stmt, DummyModel, params, sortable_columns=["name", "email"]
    )

    order_by_clauses = paginated._order_by_clauses
    assert len(order_by_clauses) == 2
    assert "DESC" in str(order_by_clauses[0])
    assert "ASC" in str(order_by_clauses[1])
