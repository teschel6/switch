from dataclasses import dataclass
from typing import List


@dataclass
class Project:
    id: str
    name: str


@dataclass
class Reference:
    id: str
    name: str
    directory: str


@dataclass
class UserConfig:
    projects: List[Reference]
