from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.db_models.category import Category


class CategoryRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_all(self) -> list[Category]:
        statement = select(Category).order_by(Category.id)

        return list(self._session.scalars(statement).all())

    def find_by_category_key(self, category_key: str) -> Category | None:
        statement = select(Category).where(Category.category_key == category_key)

        return self._session.scalars(statement).one_or_none()

    def save(self, category: Category) -> Category:
        self._session.add(category)
        self._session.commit()
        self._session.refresh(category)

        return category

    def upsert_many(self, categories: Sequence[Category]) -> int:
        if not categories:
            return 0

        values = [
            {
                "id": category.id,
                "category_key": category.category_key,
                "display_name": category.display_name,
            }
            for category in categories
        ]

        statement = insert(Category).values(values)

        statement = statement.on_conflict_do_update(
            index_elements=[Category.category_key],
            set_={
                "id": statement.excluded.id,
                "display_name": statement.excluded.display_name,
                "updated_at": func.current_timestamp(),
            },
        )

        self._session.execute(statement)
        self._session.commit()

        return len(values)
