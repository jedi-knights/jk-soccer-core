from dataclasses import dataclass


@dataclass
class Coach:
    name: str
    title: str = None
