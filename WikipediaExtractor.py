import wikipedia
import unicodedata


def get_term_dict(title, terms_list):
    count_dict = {}

    try:
        page = wikipedia.page(title)
    except:
        return count_dict

    text = unicodedata.normalize('NFKD', page.summary).encode('ascii', 'ignore')

    if text.count > 0:
        for term in terms_list:
            if term != "" and term != title:
                count = text.count(term)
                count_dict[term] = count

        counts = count_dict.values()
        return count_dict


def check_existence(dic):
    if dic:
        for value in dic.values():
            if value == 0:
                return -1
        return 1
    else:
        return -1
