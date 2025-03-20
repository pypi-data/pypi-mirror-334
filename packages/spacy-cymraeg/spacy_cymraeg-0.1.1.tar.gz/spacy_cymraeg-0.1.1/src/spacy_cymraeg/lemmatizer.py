from typing import List, Dict, Tuple

from spacy.pipeline import Lemmatizer
from spacy.tokens import Token


class WelshLemmatizer(Lemmatizer):
    """XXXX"""

    @classmethod
    def get_lookups_config(cls, mode: str) -> Tuple[List[str], List[str]]:
        if mode == "lookup":
            required = [
                "lemma_lookup_adj",
                "lemma_lookup_adp",
                "lemma_lookup_adv",
                "lemma_lookup_aux",
                "lemma_lookup_det",
                "lemma_lookup_noun",
                "lemma_lookup_num",
                "lemma_lookup_pron",
                "lemma_lookup_propn",
                "lemma_lookup_verb",
                #"lemma_lookup_other",
                #"lemma_lookup",
            ]
            return (required, [])
        else:
            return super().get_lookups_config(mode)

    def lookup_lemmatize(self, token: Token) -> List[str]:
        string = token.text
        univ_pos = token.tag_
        lookup_pos = univ_pos.lower()
        lookup_table = self.lookups.get_table("lemma_lookup_" + lookup_pos, {})
        if univ_pos == "NOUN":
            return self.lemmatize_noun(string, univ_pos, lookup_table)
        else:
            if univ_pos != "PROPN":
                string = string.lower()
            if univ_pos == "DET":
                return self.lemmatize_det(string, univ_pos, lookup_table)
            elif univ_pos == "PRON":
                return self.lemmatize_pron(string, univ_pos, lookup_table)
            elif univ_pos == "ADP":
                return self.lemmatize_adp(string, univ_pos, lookup_table)
            elif univ_pos == "ADJ":
                return self.lemmatize_adj(string, univ_pos, lookup_table)
            else:
                lemma = lookup_table.get(string, "")
        #if not lemma:
        #    lookup_table = self.lookups.get_table("lemma_lookup_other")
        #    lemma = lookup_table.get(string, "")
        #if not lemma:
        #    lookup_table = self.lookups.get_table(
        #        "lemma_lookup"
        #    )  # "legacy" lookup table
        #    lemma = lookup_table.get(string, string.lower())
        if not lemma:
            lemma = token.text
        return [lemma]
        
        
        
    def lemmatize_det(
        self, string: str, univ_pos: str, lookup_table: Dict[str, str]
    ) -> List[str]:
        return [lookup_table.get(string, string)]

    def lemmatize_pron(
        self, string: str, univ_pos: str, lookup_table: Dict[str, str]
    ) -> List[str]:
        lemma = lookup_table.get(string, string)
        return [lemma]

    def lemmatize_adp(
        self, string: str, univ_pos: str, lookup_table: Dict[str, str]
    ) -> List[str]:
        return [lookup_table.get(string, string)]

    def lemmatize_adj(
        self, string: str, univ_pos: str, lookup_table: Dict[str, str]
    ) -> List[str]:
        lemma = lookup_table.get(string, string)
        return [lemma]

    def lemmatize_noun(
        self, string: str, univ_pos: str, lookup_table: Dict[str, str]
    ) -> List[str]:
        return [lookup_table.get(string, string)]
