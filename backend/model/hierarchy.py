# Module to define specific rules for hierarchy
# The rules here are "Global" rules so they are
# not written in the database.
from dataclasses import asdict, dataclass, field
from typing import List, Optional


@dataclass
class BaseItem:
    volet: Optional[str] = None
    rubrique: Optional[str] = None
    sous_rubrique: Optional[str] = None

    def dict(self):
        return asdict(self)


@dataclass
class GlobalMark(BaseItem):
    attributes: List = field(default_factory=list)


@dataclass
class GlobalItem(BaseItem):
    attribut: str = ""
    id_attribut: int = 0
