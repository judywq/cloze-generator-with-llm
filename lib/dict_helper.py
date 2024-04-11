import os
import requests
import concurrent
from concurrent.futures import ThreadPoolExecutor
import json
import logging

output_path = './cache/dict/'
max_workers = 10

fl_to_pos = {
    'noun': 'NN',
    'verb': 'VB',
    'adjective': 'JJ',
    'adverb': 'RB',
    'pronoun': 'PRP',
    'determiner': 'DT',
    'preposition': 'IN',
    'conjunction': 'CC',
    'interjection': 'UH',
}

def fetch_words_from_dict(keywords: list[str], api_key: str):
    
    if not api_key:
        raise ValueError('Dict API key is not provided!')
    result_dict = {}
    if not keywords:
        return result_dict
    
    candidates = []
    american_spellings = []
    for keyword in keywords:
        tmp_result = try_load_from_json(keyword)
        if tmp_result is not None:
            result_dict[keyword] = tmp_result
            american_spelling = _try_get_american_spelling(json_data=tmp_result)
            if american_spelling is not None:
                american_spellings.append(american_spelling)
        else:
            candidates.append(keyword)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit requests in parallel
        future_to_keyword = {executor.submit(_fetch_dictionary_data, api_key, keyword): keyword for keyword in candidates}

        for future in concurrent.futures.as_completed(future_to_keyword):
            keyword = future_to_keyword[future]
            try:
                result = future.result()
                result_dict[keyword] = result
                if result is not None:
                    save_to_json(keyword, result)
                    american_spelling = _try_get_american_spelling(json_data=result)
                    if american_spelling is not None:
                        american_spellings.append(american_spelling)
            except Exception as e:
                logging.error(f'Error processing result for {keyword}: {e}')
    
    american_dict = fetch_words_from_dict(american_spellings, api_key)
    result_dict.update(american_dict)
    return result_dict

def _fetch_dictionary_data(api_key, keyword):
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for any errors in the HTTP response

        # Parse the JSON response
        json_data = response.json()

        return json_data

    except requests.exceptions.RequestException as e:
        logging.error(f'Error making API request for {keyword}: {e}')
        return None
    

def get_filename(keyword):
    return os.path.join(output_path, f'{keyword}.json')

def try_load_from_json(keyword):
    filename = get_filename(keyword)
    if os.path.exists(filename) == False:
        return None
    with open(filename, 'r') as file:
        logging.debug(f'Result for {keyword} loaded from {filename}')
        return json.load(file)
    

def save_to_json(keyword, data):
    if os.path.exists(output_path) == False:
        os.mkdir(output_path)
    filename = get_filename(keyword=keyword)
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)
        logging.debug(f'Result for {keyword} saved to {filename}')


def parse_json_data(json_data, headword=None):
    
    american_spelling = _try_get_american_spelling(json_data)
    if american_spelling is not None:
        json_data = try_load_from_json(american_spelling)
        headword = american_spelling
    
    result_list = []
    # Extract 'fl' (function label) and 'sense' information
    if _is_valid_json_data(json_data):
        for entry in json_data:
            fl = entry.get('fl')
            senses = entry.get('def', [])

            # print(f'Function Label: {fl}')
            id = entry.get('meta', {}).get('id')
            current_headword = id.split(':')[0]
            if headword is not None and current_headword != headword:
                continue
            
            # stems = entry.get('meta', {}).get('stems', [])
            # if headword is not None and headword not in stems:
            #     # this entry is not for the headword
            #     continue
            
            result_entry = {'id': id, 'fl': fl, 'senses': []}

            for sense in senses:
                for sseq in sense.get('sseq', []):
                    for item in sseq:
                        if isinstance(item, list) and item[0] == 'sense':
                            sn = item[1].get('sn')
                            dt = item[1].get('dt', [])
                            sense_text = ''
                            # print(f'\tSense {sn}:')
                            for text_type, text_content in dt:
                                if text_type == 'text':
                                    # print(f'\t\t{text_content}')
                                    sense_text = text_content
                            result_entry['senses'].append({'sn': sn, 'text': sense_text})
            result_list.append(result_entry)
    else:
        logging.warning(f'No valid json data found for the keyword: {headword}')    
    return result_list


def load_parsed_keyword(keyword):
    json_data = try_load_from_json(keyword)
    if json_data is None:
        logging.error(f'No data found for keyword: {keyword}. Please fetch it first.')
        return None
    
    return parse_json_data(json_data, keyword)

def get_pos_list_of_keyword(keyword):
    result_list = load_parsed_keyword(keyword)
    if result_list is None:
        return None
    pos_list = [translate_fl_to_pos(entry.get('fl')) for entry in result_list]
    return pos_list


def translate_fl_to_pos(fl):
    if isinstance(fl, str):
        fl_lower = fl.lower()
        return fl_to_pos.get(fl_lower, fl)
    return 'UNK'

def get_senses_of_keyword(keyword):
    """Get senses of a keyword, organized by pos tags

    Args:
        keyword (str): keyword to look up

    Returns:
        dict: a dictionary mapping from pos tags to a list of sense texts
    """
    result_list = load_parsed_keyword(keyword)
    sense_mapping = {}
    for entry in result_list:
        pos = translate_fl_to_pos(entry.get('fl'))
        senses = entry.get('senses', [])
        texts = [sense.get('text') for sense in senses]
        # texts = [remove_curly_braces_content(text) for text in texts]
        tmp_senses = sense_mapping.get(pos, [])
        tmp_senses.extend(texts)
        sense_mapping[pos] = tmp_senses
    return sense_mapping


def _is_valid_json_data(json_data):
    if isinstance(json_data, list) and len(json_data) > 0:
        # Check the first entry
        entry = json_data[0]
        if isinstance(entry, dict):
            return True
    return False

def _try_get_american_spelling(json_data):
    if _is_valid_json_data(json_data):
        # Check the first entry
        entry = json_data[0]
        entry.get('cxs', [])
        for cx in entry.get('cxs', []):
            if 'British spelling of' in cx.get('cxl', ''):
                american_spelling = cx.get('cxtis', [{}])[0].get('cxt', None)
                return american_spelling
        
    return None
