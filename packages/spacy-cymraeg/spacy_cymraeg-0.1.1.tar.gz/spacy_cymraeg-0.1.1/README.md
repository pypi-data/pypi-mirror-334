# Spacy Cymraeg

A package makes the `cy` language package from [github.com/techiaith/spacy/](https://github.com/techiaith/spacy/tree/welsh/spacy/lang)
installable and usable without having to modify the files within the virtual environment.

## Install package
To install the package using `uv` run the following command:
```bash
uv add spacy-cymraeg
```
or you can install the repository directly like so:
```bash
uv add git+https://gitlab.com/prvInSpace/spacy-cymraeg
```

## Using the package
The language is not loaded by default, so you need to register the language.
You can do this by adding the following line of code to your code:
```python
import spacy_cymraeg
```
By importing the package the language gets registered as `cy` which means that you can use models that depend on it
such as the `cy_techiaith_tag_lem_ner_lg` pipeline which you can find on [github.com/techiaith/spacy_cy_tag_lem_ner_lg](https://github.com/techiaith/spacy_cy_tag_lem_ner_lg).

To use the package with `cy_techiaith_tag_lem_ner_lg` please also install that package by running the following command:
```bash
uv add https://github.com/techiaith/spacy_cy_tag_lem_ner_lg/releases/download/23.03/cy_techiaith_tag_lem_ner_lg-0.0.1.tar.gz"
```

and then you can use it on code like so:
```python
import spacy
import spacy_cymraeg

nlp = spacy.load("cy_techiaith_tag_lem_ner_lg")
doc = nlp("Lansiodd David Hill Jones ei gyfrol newydd The Singularity Show yn nigwyddiad y Cyngor Llyfrau yn Aberystwyth yn gynharach heddiw.")
for item in [(t, t.lemma_, t.pos_, t.morph, t.ent_type_, t.vector_norm) for t in doc]:
    print (item)
```

**N.B.:** Note that `cy_techiaith_tag_lem_ner_lg` depends on a `numpy<2`, so make sure that you are using something like `1.26` or something.

