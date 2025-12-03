from typing import List


class Project:
    id: str
    name: str

    def __init__(self, id: str, name: str) -> None: ...

    def __str__(self):
        return f"Reference[{self.id=},{self.name=}]"


class Reference:
    id: str
    name: str
    directory: str

    def __init__(self, id: str, name: str, directory: str) -> None: ...

    def __str__(self) -> str:
        return f"Reference[{self.id=},{self.name=},{self.directory=}]"


class UserConfig:
    projects: List[Reference]

    def __init__(self, projects):
        self.projects = projects
