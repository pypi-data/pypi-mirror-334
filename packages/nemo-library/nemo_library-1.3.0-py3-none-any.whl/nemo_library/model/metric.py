from dataclasses import dataclass, asdict, field
from typing import Optional, Dict, Any, List

from nemo_library.utils.utils import get_internal_name

@dataclass
class Metric:
    aggregateBy: str = ""
    aggregateFunction: str = ""
    dateColumn: Optional[str] = ""
    description: str = ""
    descriptionTranslations: Dict[str, str] = field(default_factory=dict)
    displayName: str = ""
    displayNameTranslations: Dict[str, str] = field(default_factory=dict)
    groupByAggregations: Dict[str, str] = field(default_factory=dict)
    groupByColumn: str = ""
    isCrawlable: bool = True
    optimizationOrientation: str = ""
    optimizationTarget: bool = False
    scopeId: Optional[str] = ""
    scopeName: Optional[str] = ""
    unit: str = ""
    defaultScopeRestrictions: List[Any] = field(default_factory=list)
    focusOrder: str = ""
    internalName: str = ""
    parentAttributeGroupInternalName : str = ""
    id: str = ""
    projectId: str = ""
    tenant: str = ""

    def to_dict(self):
        return asdict(self)
    
    def __post_init__(self):
        if self.internalName is None:
            self.internalName = get_internal_name(self.displayName)
