# #import pysnooper  # type: ignore

from logging import Logger, getLogger
from typing import get_type_hints
from abc import ABC

log: Logger = getLogger(__name__)


class KConfig(ABC):
    name: str
    version: str
    display_label: str
    category: str
    description: str
    author: str
    author_email: str
    MANIFEST: dict
    DEFAULTS: dict
    _mandatory: list

    def __init__(self, *args, **kwargs):
        self._mandatory = ["name", "version", "category", "author"]
        self.name = kwargs.get("name", "")
        self.version = kwargs.get("version", "")
        self.display_label = kwargs.get("display_label", "")
        self.category = kwargs.get("category", "")
        self.description = kwargs.get("description", "")
        self.author = kwargs.get("author", "")
        self.author_email = kwargs.get("author_email", "")
        self.MANIFEST = self._format_metadata(*args)

    #   #@pysnooper.snoop()
    def _format_metadata(self, *args):
        meta = {
            "PACKAGE": {
                "NAME": self.name,
                "LABEL": self.display_label,
                "VERSION": self.version,
                "DESCRIPTION": self.description,
                "CATEGORY": self.category,
            },
            "MODULES": {},
        }
        for arg in args:
            meta["MODULES"].update({arg[0]: arg[1].manifest})
        return meta

    def recompute_package_metadata(self, *args, **kwargs):
        self.MANIFEST = self._format_metadata(*args, **kwargs)
        return self.MANIFEST

    def metadata(self):
        return get_type_hints(self, include_extras=True)

    def data(self):
        return self.__dict__
