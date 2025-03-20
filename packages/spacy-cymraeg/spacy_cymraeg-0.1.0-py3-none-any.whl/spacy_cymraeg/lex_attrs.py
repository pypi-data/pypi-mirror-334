from spacy.attrs import LIKE_NUM

# TODO: Deal with multi word numbers such as 'un ar ddeg' (eleven)

_num_words = (
    'sero',
    'un',
    'dau', 'ddau', 'nau', 'dwy', 'ddwy', 'nwy',
    'tri', 'dri', 'thri', 'tair', 'dair', 'thair',
    'pedwar', 'bedwar', 'phedwar', 'pedair', 'bedair', 'phedair',
    'pump', 'bump', 'phump', 'pum', 'bum', 'phum',
    'chwech', 'chwe',
    'saith',
    'wyth',
    'naw',
    'deg', 'ddeg', 'deng', 'ddeng',
    'deuddeg', 'ddeuddeg', 'deuddeng', 'ddeuddeng',
    'pymtheg', 'bymtheg', 'phymtheg', 'pymtheng', 'bymtheng', 'phymtheng',
    'deunaw', 'ddeunaw', 'neunaw',
    'ugain', 'hugain',
    'deugain', 'ddeugain', 'neugain',
    'trigain', 'drigain', 'thrigain',
    'cant', 'gant', 'chant', 'can', 'gan', 'chan',
    'mil', 'fil',
    'miliwn', 'filiwn',
    'biliwn',
    'triliwn', 'driliwn', 'thriliwn',
    'cwadriliwn', 'gwadriliwn', 'chwadriliwin')


def like_num(text):
    text = text.replace(',', '').replace('.', '')
    if text.isdigit():
        return True
    if text.count('/') == 1:
        (num, denom) = text.split('/')
        if num.isdigit() and denom.isdigit():
            return True
    return text in _num_words


LEX_ATTRS = {
    LIKE_NUM: like_num
}
