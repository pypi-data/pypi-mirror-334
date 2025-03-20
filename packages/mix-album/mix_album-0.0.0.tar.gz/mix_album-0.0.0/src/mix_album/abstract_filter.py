# abstract_filter.py
#
# Project: Mix Album
# License: GNU GPLv3
# Copyright (C) 2024 - 2025 Róbert Čerňanský



from abc import ABC, abstractmethod

from mix_album.medium import Medium



class AbstractFilter(ABC):

    @property
    @abstractmethod
    def argumentName(cls) -> str:
        pass



    @property
    @abstractmethod
    def description(cls) -> str:
        pass



    @property
    @abstractmethod
    def argumentHelp(cls) -> str:
        pass



    @abstractmethod
    def canParseArgument(cls, argument: str) -> bool:
        pass



    @abstractmethod
    def apply(self, medium: Medium) -> Medium:
        pass
