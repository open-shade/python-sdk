from abc import ABC
from dataclasses import dataclass


@dataclass
class ABCResource(ABC):
    auth: 'Shade'
