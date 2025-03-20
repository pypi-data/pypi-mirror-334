# encoding: utf8
from typing import Dict, List

from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS
from spacy.util import update_exc
from spacy.symbols import ORTH, NORM


_exc: Dict[str, List[Dict]] = {}

_exc_datums = [
    {ORTH: "ion.", NORM: "Ionawr"},
    {ORTH: "chw.", NORM: "Chwefror"},
    {ORTH: "maw.", NORM: "Mawrth"},
    {ORTH: "ebr.", NORM: "Ebrill"},
    {ORTH: "mai.", NORM: "Mai"},
    {ORTH: "meh.", NORM: "Mehefin"},
    {ORTH: "gor.", NORM: "Gorffenaf"},
    {ORTH: "aws.", NORM: "Awst"},
    {ORTH: "med.", NORM: "Medi"},
    {ORTH: "hyd.", NORM: "Hydref"},
    {ORTH: "tac.", NORM: "Tachwedd"},
    {ORTH: "rha.", NORM: "Rhagfyr"},
    {ORTH: "St.", NORM: "Sant"},
    {ORTH: "Dr.", NORM: "Doctor"},
]

for exc_data in _exc_datums:
    _exc[exc_data[ORTH]] = [exc_data]


TOKENIZER_EXCEPTIONS = update_exc(BASE_EXCEPTIONS, _exc)
