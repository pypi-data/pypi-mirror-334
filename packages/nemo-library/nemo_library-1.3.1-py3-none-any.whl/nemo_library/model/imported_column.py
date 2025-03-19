from dataclasses import dataclass, asdict, field
from typing import Optional

from nemo_library.utils.utils import get_import_name, get_internal_name


@dataclass
class ImportedColumn:
    categorialType: bool = False
    columnType: str = "ExportedColumn"
    containsSensitiveData: bool = False
    dataType: str = "string"
    description: str = ""
    displayName: str = None
    formula: str = ""
    groupByColumnInternalName: Optional[str] = field(default_factory=str)
    importName: str = None
    stringSize: int = 0
    unit: str = ""
    focusOrder: str = ""
    internalName: str = None
    parentAttributeGroupInternalName: str = None
    id: str = ""
    projectId: str = ""
    tenant: str = ""

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):
        if self.importName is None:
            self.importName = get_import_name(self.displayName)

        if self.internalName is None:
            self.internalName = get_internal_name(self.displayName)
