from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class Visual:
    column: int
    columnSpan: int
    content: str
    contentTranslations: Dict[str, str]
    id: str
    row: int
    rowSpan: int
    type: str

@dataclass
class Page:
    description: str
    descriptionTranslations: Dict[str, str]
    displayName: str
    displayNameTranslations: Dict[str, str]
    hideIfColumns: List[str]
    internalName: str
    numberOfColumns: int
    numberOfRows: int
    showIfColumns: List[str]
    visuals: List[Visual]
    id: str
    projectId: str
    tenant: str

    def to_dict(self):
        return asdict(self)