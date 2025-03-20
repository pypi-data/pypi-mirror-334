import logging

from abc import ABC
from typing import Annotated, get_type_hints

from kaya_module_sdk.src.utils.metadata.display_description import DisplayDescription
from kaya_module_sdk.src.utils.metadata.display_name import DisplayName

log = logging.getLogger(__name__)


class Args(ABC):
    _errors: Annotated[
        list,
        DisplayName("Errors"),
        DisplayDescription("Collection of things that went very, very wrong."),
    ]

    _live: Annotated[
        bool,
        DisplayName("Live Execution"),
        DisplayDescription(
            "Input provided by the Systemic runtime. Indicates if the current request is a historical"
            "backfilling request, or a LIVE execution request. Live requests should only return the"
            "last computed datapoint"
        ),
    ]

    def __init__(self):
        self._errors = []
        self._live = True

    @property
    def errors(self) -> list[Exception]:
        return self._errors

    @property
    def live(self) -> bool:
        return self._live

    def set_errors(self, *values: Exception) -> None:
        self._errors += list(values)

    def set_live(self, value: bool) -> None:
        self._live = value

    def metadata(self):
        return get_type_hints(self, include_extras=True)
