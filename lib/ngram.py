import requests

from lib.utils import get_general_pos


google_pos_to_penn_pos = {
    "NOUN": "NN",
    "VERB": "VB",
    "ADJ": "JJ",
    "ADV": "RB",
}

penn_pos_to_google_pos = {
    "NN": "NOUN",
    "VB": "VERB",
    "JJ": "ADJ",
    "RB": "ADV",
}


def filter_high_freq_pos(headword, pos_list, th=0.1):
    """Filter out pos tags with frequency less than a percentage of the highest frequency
    
    returns a list of general pos tags that have high frequency
    """
    res = []
    item_list = []
    searchitem_to_pos_mapping = {}
    for pos in pos_list:
        general_pos = get_general_pos(pos)
        g_pos = penn_pos_to_google_pos.get(general_pos, None)
        search_item = f"{headword}_{g_pos}"
        if g_pos is not None and search_item not in searchitem_to_pos_mapping:
            searchitem_to_pos_mapping[search_item] = general_pos
            item_list.append(search_item)
    content = ",".join(item_list)
    last_values = search_ngram(content)
    if not last_values:
        return res
    top_record = max(last_values, key=lambda x: x["last_value"])
    top_value = top_record["last_value"]
    th_value = top_value * th

    for record in last_values:
        if record["last_value"] >= th_value:
            tag = searchitem_to_pos_mapping.get(record["ngram"], None)
            res.append(tag) if tag is not None else None
    return res


def filter_high_freq_inflections(inf_data, th=0.1):
    tagword_to_searchitem_mapping = {}
    item_list = []
    for tag, words in inf_data.items():
        g_pos = penn_pos_to_google_pos.get(get_general_pos(tag), None)
        if g_pos is not None:
            for w in words:
                search_item = f"{w}_{g_pos}"
                tagword_to_searchitem_mapping[(tag, w)] = search_item
                item_list.append(search_item)

    content = ",".join(item_list)
    last_values = search_ngram(content)
    
    if not last_values:
        return inf_data

    top_record = max(last_values, key=lambda x: x["last_value"])
    top_value = top_record["last_value"]
    th_value = top_value * th
    result = {}
    for tag, words in inf_data.items():
        g_pos = penn_pos_to_google_pos.get(get_general_pos(tag), None)
        if g_pos is not None:
            for w in words:
                search_item = tagword_to_searchitem_mapping[(tag, w)]
                for record in last_values:
                    if record["ngram"] == search_item:
                        if record["last_value"] >= th_value:
                            word_set = result.get(tag, set())
                            word_set.add(w)
                            result[tag] = word_set
    return result
    


def get_last_timeseries(json_data):
    last_values = []
    for record in json_data:
        ngram = record["ngram"]
        ngram_type = record["type"]
        timeseries = record["timeseries"]
        last_value = timeseries[-1]
        
        last_values.append({"ngram": ngram, "type": ngram_type, "last_value": last_value})
        # last_values[ngram] = {"type": ngram_type, "last_value": last_value}
    return last_values


def search_ngram(content, year_start=2018, year_end=2019, corpus="en-2019", smoothing=3):
    url = "https://books.google.com/ngrams/json"

    try:
        response = requests.get(url, params={
            "content": content,
            "year_start": year_start,
            "year_end": year_end,
            "corpus": corpus,
            "smoothing": smoothing
        })
        response.raise_for_status()
        json_data = response.json()

        last_values = get_last_timeseries(json_data)

        for item in last_values:
            ngram = item["ngram"]
            ngram_type = item["type"]
            last_value = item["last_value"]
            print(f"Ngram: {ngram}, Type: {ngram_type}, Last Value: {last_value}")
        
        return last_values

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        return []

