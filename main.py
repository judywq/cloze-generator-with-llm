import pandas as pd
from lib.chat import MyBotWrapper
from lib.parser import SentGenParser, DerivativeParser, RationalParser, PosTagParser
from lib.utils import get_date_str, setup_log, setup_randomness
from lib.io import read_data, write_data
from lib.word_cluster import WordCluster
from setting import DISTRACTOR_COUNT, KEYWORD_START_POS, TEST_DISTRACTOR_COUNT, KEYWORD_COUNT

import logging
logger = logging.getLogger(__name__)


def main():
    now = get_date_str()
    path = 'data/input/AWL.xlsx'
    sublist = 1
    fn_data = f'./data/output/{now}-AWL-sublist-{sublist}-cloze.xlsx'
    fn_log = f'./log/excel/{now}-log.xlsx'
    fn_inflections = f'./log/excel/{now}-inflections.xlsx'
    inflection_columns = ['word', 'tag', 'lemm', 'unimorph', 'chatgpt']

    logger.info(f"Loading data from {path}...")
    word_cluster = load_sublist(path, sublist=sublist)
    df_inflections = pd.DataFrame(word_cluster.inflection_log, columns=inflection_columns)
    write_data(df_inflections, fn_inflections)
    logger.info(f"Inflections saved to {fn_inflections}")
    return
    
    words = select_keywords(word_cluster, start=KEYWORD_START_POS, max_count=KEYWORD_COUNT)
    n_total = len(words)
    logger.info(f"Start generating cloze sentences for {n_total} words...")

    bot_sent_gen = MyBotWrapper(parser=SentGenParser(), temperature=0.9)
    # bot_derive = MyBotWrapper(parser=DerivativeParser(), temperature=0.1)
    bot_rational = MyBotWrapper(parser=RationalParser(), temperature=0)

    log_columns = ['Date', 'Task', 'Keyword', 'Tag', 'Prompt', 'Raw Response', 'Parsed Result', 'Success']
    log_data = []
    
    columns = ['Sentence', 'Correct Answer', *[f'Distractor {i}' for i in range(1, DISTRACTOR_COUNT+1)]]
    data = []
    for i, word in enumerate(words):
        
        keyword = word.surface
        keyword_tag = word.tag
        # print(f"{repr(w)}: {candidates}")
        r = bot_sent_gen.run(inputs={"word": keyword, "tag": keyword_tag})
        suc = r.get('success')
        log_data.append([get_date_str(), bot_sent_gen.task_name, word.surface, word.tag, r.get('prompt'), r.get('raw_response'), r.get('result'), suc])
        if not suc:
            logger.error(f"Failed to generate sentence for '{keyword}'")
            continue
        sentence = r.get('result')
        
        distractors = fill_distractors(bot_rational, word_cluster, word, sentence, log_data=log_data)
        
        data.append([sentence, keyword, *distractors])

        msg = "\n".join([f"{i+1}/{n_total}: " + "-" * 80,
                f"Sentence: {sentence}",
                f"Keyword: {keyword}",
                "Distractors: " + ", ".join(distractors),])
        logger.info(msg)
        
        df = pd.DataFrame(data, columns=columns)
        write_data(df, fn_data)

        df_log = pd.DataFrame(log_data, columns=log_columns)
        write_data(df_log, fn_log)
    
    logger.info(f"Done. Data saved to {fn_data}")


def fill_distractors(bot_rational, word_cluster, word, sentence, log_data=[], max_trials=5):
    excepts = [word]
    distractors = []
    for i in range(max_trials):
        candidates = word_cluster.find_distractors(word.tag, excepts=excepts, n=TEST_DISTRACTOR_COUNT)
        excepts += candidates
        
        if len(candidates) == 0:
            logger.warning(f"No more distractor candidates for '{word}'")
            break
        
        r = bot_rational.run(inputs={"words": candidates, "sentence": sentence})
        suc = r.get('success')
        good_candidates = r.get('good_candidates')
        log_data.append([get_date_str(), bot_rational.task_name, word.surface, word.tag, r.get('prompt'), r.get('raw_response'), good_candidates, suc])
        if not suc:
            logger.error(f"Failed to decide proper distractors for {word}")
            continue
        # Make sure the distractors do not exceed the max count
        distractors += [str(w) for w in good_candidates]
        
        if len(distractors) == DISTRACTOR_COUNT:
            break
        elif len(distractors) > DISTRACTOR_COUNT:
            distractors = distractors[:DISTRACTOR_COUNT]
            break
        else:
            logger.debug(f"Trial {i}: {len(distractors)} distractors collected in total.")
    return distractors


def load_sublist(path, sublist=1, max_count=-1):
    """Load a sublist from a file as a WordCluster object
    """
    df = read_data(path=path)
    df = df[df['Sublist'] == sublist]
    df = df.astype({'Headword': 'str', 'Related word forms': 'str'})
    wc = WordCluster()
    for i, row in df.iterrows():
        headword = row['Headword']
        logger.info(f"Processing word family for '{headword}'...")
        # related_words = row['Related word forms'].split(',')
        # Do not derive for now
        related_words = []
        wc.add_item(headword, related_words)
        if max_count > 0 and i >= max_count:
            break
    logger.debug("Shape of data: {}\n{}".format(df.shape, df.head()))
    # wc.print()
    return wc


def select_keywords(word_cluster: WordCluster, start=0, max_count=-1):
    words = []
    for wf in word_cluster.word_family_list[start:]:
        w = wf.get_random_word()
        # w = wf.headword
        words.append(w)
        if max_count > 0 and len(words) >= max_count:
            break
    return words
################################

    
if __name__ == '__main__':
    setup_randomness()
    setup_log()
    main()
