from os.path import dirname, abspath
import sys

import pandas as pd
 
directory = dirname(dirname(abspath(__file__)))
# https://www.geeksforgeeks.org/python-import-from-parent-directory/
sys.path.append(directory)

# import lib.io
from lib.io import read_data
from lib.word_cluster import WordCluster
from lib.inflections import try_filter_high_freq_pos, try_filter_high_freq_noun, get_inflections, get_inflections_lemm, get_inflections_unimorph
# from pyinflect import getAllInflections, getInflection
# from lemminflect import getAllInflections, getInflection
from pprint import pprint


def test1():
    import spacy
    # python -m spacy download en_core_web_sm
    nlp = spacy.load('en_core_web_sm')
    # https://pypi.org/project/pyinflect/
    doc = nlp('This is an example.')
    print(doc[3].tag_)                # NN
    print(doc[3]._.inflect('NNS'))    # examples


def test_libs():
    w = 'happily'
    w = 'greatly'
    w = 'police'
    
    lemm = get_inflections_lemm(w)
    print('---- lemm')
    pprint(lemm)
    
    unimorph = get_inflections_unimorph(w)
    print('---- unimorph')
    pprint(unimorph)

def test_single_word():
    w = 'approach'
    w = 'available' # This word has no record in pyinflect
    # w = 'availability'
    # w = 'account'
    # w = 'constitute'
    w = 'area'
    w = 'formula'
    w = 'distribute'
    w = 'economy'
    w = 'indicate'
    w = 'finance'
    w = 'sector'
    w = 'contextualize'
    w = 'analyze'
    # w = 'beneficial'
    # w = 'whereas'
    w = 'conceptualisation'
    w = 'analyser'
    w = 'constitutional'
    w = 'distributive'
    # w = 'functional'
    # w = 'redistribution'
    # w = 'reinterpretation'
    w = 'police'
    w = 'fish'
    w = 'measure'
    w = 'disaster'
    w = 'dog'
    w = 'human'
    w = 'eriee'
    # w = 'robot'
    tag_to_words, log = get_inflections(w)
    print(",".join(tag_to_words.keys()))
    df = pd.DataFrame(log)
    print(df)


def test_filter_inflections_by_pos():
    headword = 'account'
    tag_to_words = {
        'NN': {'account'},
        'NNS': {'accounts'},
        'VB': {'account'},
        'VBP': {'account'},
        'VBZ': {'accounts'},
        'JJ': {'account'},
    }
    res = try_filter_high_freq_pos(headword, tag_to_words)
    print(res)

def test_filter_inflections_by_noun_pos():
    tag_to_words = {
        'NN': {'fish'},
        'NNS': {'fishes'},
        'VB': {'fish'},
        'VBP': {'fish'},
        'VBZ': {'fishes'},
    }
    res = try_filter_high_freq_noun(tag_to_words)
    print(res)

def test_several_words():
    words = [
        'available',
        'data',
        'similar',
    ] # These words have no record in pyinflect
    
    # These words have no record in lemminflect
    words =  ['criteria', 'despite', 'whereas', 'albeit', 'so-called']
    for w in words:
        res = get_inflections(w)
        print(w)
        pprint(res)



def test_tags_awl():
    path = "data/input/AWL.xlsx"
    df = read_data(path)
    df = df[df['Sublist'] == 1]
    df = df.astype({'Headword': 'str', 'Related word forms': 'str'})
    wc = WordCluster()
    for i, row in df.iterrows():
        headword = row['Headword']
        wc.add_item(headword)
    
    # wc.print()
    wf = wc.word_family_list[36]
    wf.print()
    w = list(wf.all_words)[0]
    
    excepts = [w]
    cands = wc.find_distractors(w.tag, excepts, n=-1)
    cands
    s = set(cands)
    excepts += cands
    excepts
    
    len(wc.tag_to_words.get('JJ'))
    
    wc.find_distractors(w.tag)
    
    print(f"tag size: {wc.tag_size}")

def test_reliability():
    path = "data/input/AWL.xlsx"
    df = read_data(path)
    ng = []
    for _, row in df.iterrows():
        w = row['Headword']
        res, log = get_inflections(w)
        if not res:
            ng.append(w)
    if len(ng) > 0:
        print(f"{len(ng)} words are not found in inflect lib:\n {ng}")
    else:
        print("All words are found in inflect lib.")
    

if __name__ == '__main__':
    # test1()
    # test_libs()
    test_single_word()
    # test_filter_inflections_by_pos()
    # test_filter_inflections_by_noun_pos()
    # test_several_words()
    # test_tags_awl()
    # test_reliability()
    