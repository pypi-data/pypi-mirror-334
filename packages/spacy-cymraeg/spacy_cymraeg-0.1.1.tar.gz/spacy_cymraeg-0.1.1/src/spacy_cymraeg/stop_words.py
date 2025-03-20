# Set gychwynnol - angen gwneud hyn yn iawn
# encoding: utf8

ADPS = {
    "'n",
    "ag",
    "am",
    "ar",
    "arnaf",
    "at",
    "dan",
    "dros",
    "drwy",
    "gan",
    "gyda",
    "heb",
    "hyd",
    "i",
    "mewn",
    "o",
    "tros",
    "wedi",
    "wrth",
    "ym",
    "yn",
    "yng",
    "â",
}

ADVS = {
    "beth",
    "ble",
    "llawer",
    "lle",
    "yma",
    "yna",
}

AUXS = {
	"bod",
	"byddaf",
	"mae",
	"sy",
	"sydd",
	"ydwyf",
    "yw",
}

# Careful! Can also mean 'an age', 'a stone'
AMBIGS = {
	"maen",
    "oes",
}

CONJS = {
	"ac",
	"fel",
	"neu",
	"ond",
	"os",
	"tra",
    "a",
}

DETS = {
	"'r",
	"yr",
    "y",
}

NOUNS = {
    "ôl",
    "tu"
}

PARTS = {
	"nid",
	"nis",
    "na",
}

PRONS = {
	"hi",
	"hun",
	"hyn",
	"i",
	"nhw",
	"ni",
	"pob",
    "di",
    "dy",
    "ef",
    "ei",
    "eich",
    "ein",
    "fe",
    "fy",
    "hwy"
}

STOP_WORDS = set(ADPS | ADVS | AUXS | AMBIGS | CONJS | DETS | NOUNS | PARTS | PRONS)
