from dataclasses import dataclass, asdict
from typing import Dict, List

@dataclass
class Argument:
    aggregation: str
    column: str
    dataType: str

@dataclass
class Value:
    aggregation: str
    chartType: str
    column: str
    id: str
    legend: str
    legendTranslations: Dict[str, str]

@dataclass
class Diagram:
    alternateVisualization: bool
    argument: Argument
    argumentAxisTitle: str
    argumentAxisTitleTranslations: Dict[str, str]
    description: str
    descriptionTranslations: Dict[str, str]
    displayName: str
    displayNameTranslations: Dict[str, str]
    internalName: str
    report: str
    summary: str
    valueAxisTitle: str
    valueAxisTitleTranslations: Dict[str, str]
    values: List[Value]
    id: str
    projectId: str
    tenant: str

    def to_dict(self):
        return asdict(self)
