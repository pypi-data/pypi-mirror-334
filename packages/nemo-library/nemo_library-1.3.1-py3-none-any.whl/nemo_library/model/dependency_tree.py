from dataclasses import asdict, dataclass, field
from typing import List, Optional
import json

@dataclass
class DependencyTree:
    dependencies: List[Optional["DependencyTree"]] = field(default_factory=list)
    dependencyType: Optional[str] = None
    nodeConflictState: str = ""
    nodeDisplayName: str = ""
    nodeId: str = ""
    nodeInternalName: str = ""
    nodeType: str = ""

    @staticmethod
    def from_dict(data: dict) -> "DependencyTree":
        dependencies = [DependencyTree.from_dict(dep) for dep in data.get("dependencies", [])] if "dependencies" in data else []
        return DependencyTree(
            dependencies=dependencies,
            dependencyType=data.get("dependencyType"),
            nodeConflictState=data.get("nodeConflictState", ""),
            nodeDisplayName=data.get("nodeDisplayName", ""),
            nodeId=data.get("nodeId", ""),
            nodeInternalName=data.get("nodeInternalName", ""),
            nodeType=data.get("nodeType", ""),
        )

    def to_dict(self):
        return asdict(self)
