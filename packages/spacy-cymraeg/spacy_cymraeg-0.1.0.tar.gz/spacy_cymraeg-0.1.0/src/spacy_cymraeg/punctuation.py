from typing import List

from spacy.lang.char_classes import ALPHA, HYPHENS
from spacy.lang import punctuation as punc_defaults


def _fixes(seq: List[str]):
    lowers = list(map(str.lower, seq))
    uppers = list(map(str.upper, lowers))
    lower_curly = list(s.replace("'", "’") for s in lowers)
    upper_curly = list(map(str.upper, lower_curly))
    return lowers + uppers + lower_curly + upper_curly

# isod ddim yn cydio
_prefixes = _fixes(["f'", "d'"])

TOKENIZER_PREFIXES = punc_defaults.TOKENIZER_PREFIXES + _prefixes

_suffixes = _fixes(["'ch", "'i", "'m", "'n", "'r", "'th", "'u", "'w"])

TOKENIZER_SUFFIXES = punc_defaults.TOKENIZER_SUFFIXES + _suffixes


# Infix handling - Preserve hyphenated words.
# ------------------------------------------------------------------------------------------------
# Welsh uses hyphens within words to indicate stress and to
# differentiate between digraphs and two single-grapheme letter.
# e.g: cyd-destun (two Ds) and cuddio (one DD).
#
# The folowing rule needs to be updated if the corresponding code changes in the module:
#    spacy.lang.punctuation
#
# Source of idea:
# https://stackoverflow.com/questions/55241927/spacy-intra-word-hyphens-how-to-treat-them-one-word
# ------------------------------------------------------------------------------------------------

_default_hyphenation_rule = "(?<=[{a}])(?:{h})(?=[{a}])".format(a=ALPHA, h=HYPHENS)


def _strip_default_hyphenation_rule(hyphenation_rule: str) -> List[str]:
    for infp in punc_defaults.TOKENIZER_INFIXES:
        if hyphenation_rule in infp:
            yield infp.replace(hyphenation_rule, "")
        else:
            yield infp


TOKENIZER_INFIXES = list(_strip_default_hyphenation_rule(_default_hyphenation_rule))
