from dataclasses import asdict, dataclass, field
from typing import List, Dict

from nemo_library.utils.utils import get_internal_name


@dataclass
class Report:
    columns: List[str] = field(default_factory=list)
    description: str = ""
    descriptionTranslations: Dict[str, str] = field(default_factory=dict)
    displayName: str = None
    displayNameTranslations: Dict[str, str] = field(default_factory=dict)
    internalName: str = None
    querySyntax: str = None
    reportCategories: List[str] = field(default_factory=list)
    id: str = ""
    projectId: str = ""
    tenant: str = ""

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):

        if self.internalName is None:
            self.internalName = get_internal_name(self.displayName)
            
        self.columns = [col.upper() for col in self.columns]
