from dataclasses import dataclass, asdict, field
from typing import Dict

from nemo_library.utils.utils import get_internal_name


@dataclass
class AttributeGroup:
    attributeGroupType: str = "Standard"
    defaultMetricGroup: bool = False
    defaultDefinedColumnGroup: bool = False
    displayName: str = None
    displayNameTranslations: Dict[str, str] = field(default_factory=dict)
    isCoupled: bool = False
    focusOrder: str = ""
    internalName: str = None
    parentAttributeGroupInternalName: str = ""
    id: str = ""
    projectId: str = ""
    tenant: str = ""

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):

        if self.internalName is None:
            self.internalName = get_internal_name(self.displayName)
