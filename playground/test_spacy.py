import spacy

# Run this command first:
# pipenv shell
# python -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")

def print_all_tags():
    # https://machinelearningknowledge.ai/tutorial-on-spacy-part-of-speech-pos-tagging/
    tag_lst = nlp.pipe_labels['tagger']

    print(len(tag_lst))
    print(tag_lst)
    # ['$', "''", ',', '-LRB-', '-RRB-', '.', ':', 'ADD', 'AFX', 'CC', 'CD', 'DT', 'EX', 'FW', 'HYPH', 'IN', 'JJ', 'JJR', 'JJS', 'LS', 'MD', 'NFP', 'NN', 'NNP', 'NNPS', 'NNS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB', 'XX', '_SP', '``']

def test1():
    # https://spacy.io/usage/linguistic-features
    doc = nlp("Apple is looking at buying U.K. startup for $1 billion")

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)
"""
Apple Apple PROPN NNP nsubj Xxxxx True False
is be AUX VBZ aux xx True True
looking look VERB VBG ROOT xxxx True False
at at ADP IN prep xx True True
buying buy VERB VBG pcomp xxxx True False
startup startup NOUN NN dep xxxx True False
for for ADP IN prep xxx True True
$ $ SYM $ quantmod $ False False
1 1 NUM CD compound d False False
billion billion NUM CD pobj xxxx True False    
"""    


def test_sentences():
    sentences = [
        "Dog and human are close friends.",
        "We can take measure for disaster.",
        ]
    for s in sentences:
        print_tag_of_sent(s)
        print('-'*20)

def print_tag_of_sent(sentence):
    # https://spacy.io/usage/linguistic-features
    doc = nlp(sentence)

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)


def test_sentence():
    # https://spacy.io/usage/linguistic-features
    doc = nlp("He saw a broken table.")
    doc = nlp("As winter holidays approach, many students plan trips to experience different cultures and relax")

    for token in doc:
        print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
                token.shape_, token.is_alpha, token.is_stop)

def print_spacy_tags():
    # https://machinelearningknowledge.ai/tutorial-on-spacy-part-of-speech-pos-tagging/
    doc = nlp("Get busy living or get busy dying.")
    doc = nlp("approachable")
    doc = nlp("Put it back!")
    # The VBN can be detected correctly:
    doc = nlp("The data from the research was meticulously analysed to draw precise conclusions.")
    doc = nlp("The government's proposed policies aim to reduce income inequality and improve labour conditions for workers across industries.")
    doc = nlp("The research project aims to examine the impact of technology adoption on productivity levels and labour efficiency in the manufacturing industry.")

    print(f"{'text':{8}} {'lemma':{8}} {'POS':{6}} {'TAG':{6}} {'Dep':{6}} {'POS explained':{20}} {'tag explained'} ")
    for token in doc:
        print(f'{token.text:{8}} {token.lemma_:{8}} {token.pos_:{6}} {token.tag_:{6}} {token.dep_:{6}} {spacy.explain(token.pos_):{20}} {spacy.explain(token.tag_)}')
"""
text     lemma    POS    TAG    Dep    POS explained        tag explained 
Get      get      VERB   VB     ROOT   verb                 verb, base form
busy     busy     ADJ    JJ     acomp  adjective            adjective (English), other noun-modifier (Chinese)
living   live     VERB   VBG    xcomp  verb                 verb, gerund or present participle
or       or       CCONJ  CC     cc     coordinating conjunction conjunction, coordinating
get      get      VERB   VB     conj   verb                 verb, base form
busy     busy     ADJ    JJ     amod   adjective            adjective (English), other noun-modifier (Chinese)
dying    die      VERB   VBG    dobj   verb                 verb, gerund or present participle
.        .        PUNCT  .      punct  punctuation          punctuation mark, sentence closer
"""


if __name__ == '__main__':
    # print_all_tags()
    # test1()
    # print_spacy_tags()
    # test_sentence()
    test_sentences()



