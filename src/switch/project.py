from typing import List
from dataclasses import dataclass


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
