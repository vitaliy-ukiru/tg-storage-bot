from dataclasses import dataclass


@dataclass(frozen=True)
class CreateCategoryDTO:
    user_id: int
    title: str
    desc: str | None
