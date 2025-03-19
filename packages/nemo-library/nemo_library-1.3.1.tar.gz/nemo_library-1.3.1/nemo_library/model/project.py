from dataclasses import asdict, dataclass, field
import re
from typing import List, Dict, Optional
from datetime import datetime
from uuid import UUID


@dataclass
class ColumnDetails:
    displayName: str
    id: UUID
    internalName: str


@dataclass
class ErrorDetails:
    fileOnlyColumns: List[ColumnDetails]
    id: UUID
    metadataOnlyColumns: List[ColumnDetails]


@dataclass
class Warning:
    columnId: UUID
    databaseDataType: str
    fieldName: str
    fieldNumber: int
    fieldValue: str
    id: UUID
    maxLength: int
    metadataDataType: str
    rawRowNumber: int
    rowNumber: int


@dataclass
class DataSourceImportRecord:
    endDateTime: datetime
    errorDetails: ErrorDetails
    errorType: str
    id: UUID
    recordsOmittedDueToWarnings: int
    startedByUsername: str
    status: str
    uploadId: str
    warnings: List[Warning]


@dataclass
class ProjectProperty:
    key: str
    projectId: UUID
    tenant: str
    value: str


@dataclass
class Project:
    autoDataRefresh: bool = True
    dataSourceImportRecords: List[DataSourceImportRecord] = field(default_factory=list)
    description: str = ""
    descriptionTranslations: Dict[str, str] = field(default_factory=dict)
    displayName: str = None
    displayNameTranslations: Dict[str, str] = field(default_factory=dict)
    id: str = ""
    importErrorType: str = "NoError"
    projectProperties: List[ProjectProperty] = field(default_factory=list)
    s3DataSourcePath: str = ""
    showInitialConfiguration: bool = False
    status: str = "Active"
    tableName: str = None
    tenant: str = ""
    type: str = "IndividualData"

    def to_dict(self):
        return asdict(self)

    def __post_init__(self):

        if not self.tableName:
            self.tableName = re.sub(
                r"[^A-Z0-9_]", "_", self.displayName.upper()
            ).strip()
            if not self.tableName.startswith("PROJECT_"):
                self.tableName = "PROJECT_" + self.tableName
