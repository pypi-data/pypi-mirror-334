from dataclasses import dataclass, asdict, field
from typing import Dict, List

from nemo_library.utils.utils import get_internal_name


@dataclass
class Forecast:
    groupBy: str
    metric: str


@dataclass
class PageReference:
    order: int
    page: str


@dataclass
class Application:
    active: bool = True
    description: str = ""
    descriptionTranslations: Dict[str, str] = field(default_factory=dict)
    displayName: str = None
    displayNameTranslations: Dict[str, str] = field(default_factory=dict)
    download: str = ""
    forecasts: List[Forecast] = field(default_factory=list)
    formatCompact: bool = False
    internalName: str = None
    links: List[str] = field(default_factory=list)
    models: List[str] = field(default_factory=list)
    pages: List[PageReference] = field(default_factory=list)
    scopeName: str = ""
    id: str = ""
    projectId: str = ""
    tenant: str = ""

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):

        if self.internalName is None:
            self.internalName = get_internal_name(self.displayName)
