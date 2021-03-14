import requests
from bs4 import BeautifulSoup
import csv
import re

# I dunno how to work with Globals so this might be incorrect
global url_gen
global links
links = []


def get_html(url):
    r = requests.get(url)
    return r


# in case we want to export data to .CSV file
# def write_csv(data):
#     with open('citations_info.csv', 'a') as f:
#         writer = csv.writer(f, delimiter=';')
#         writer.writerow((data['title'],
#                          data['year'],
#                          data['authors'],
#                          url_gen))


def generate_citation(data):
    one_link = (data['first_auth'][0] + ". " + data['title'] +
                " / " + data['authors'] + " // " + data['journal'] +
                " – " + data['year'] + '. – ' +
                data['volume'] + ' – C.' + data['pages'])
    print(one_link)
    links.append(one_link)


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')

    try:
        article_name = soup.find('div', class_='rprt abstract').find('h1').getText()
    except:
        article_name = ''

    try:
        temp = soup.find('div', class_='auths')
        for sup in temp.find_all('sup'):  # delete <sup> so we don't get '1','2',.. in names
            sup.decompose()
        authors_string = temp.getText()
        authors_list = temp.find_all(text=True)
    except:
        authors_string = ''
        authors_list = []

    try:
        full_citation = soup.find('div', class_='cit').getText()
        # "Rev Neurol (Paris). 2016 Aug - Sep;172(8-9):416-422. doi: 10.1016/j.neurol.2016.07.010. Epub 2016 Aug 22."

        journal_long = soup.find('div', class_='cit').find(title=True).get('title')  # "Revue neurologique."
        journal_long = journal_long[:-1]  # Without dot in the end "Revue neurologique"
        journal_short = soup.find('div', class_='cit').find(text=True)  # "Rev Neurol (Paris)."

        year_start = len(journal_short) + 1
        year_end = len(journal_short) + 5
        year_of_publication = full_citation[year_start:year_end]  # 2016

        short_citation = full_citation[year_end + 1:]
        # "Aug - Sep;172(8-9):416-422. doi: 10.1016/j.neurol.2016.07.010. Epub 2016 Aug 22."
        semicolon = short_citation.find(';')  # position of 1st semicolon
        dot = short_citation.find('.')  # position of 1st dot
        colon = short_citation.find(':')  # position of 1st colon
        journal_volume = short_citation[semicolon + 1:colon]  # "172(8-9)"
        journal_pages = short_citation[colon + 1:dot + 1]  # "416-422."

        # now i want to split journal_volume to get smth like "Vol. 172, No 8–9." (in case we got No in brackets!)
        if journal_volume.find('(') != -1:
            bracket_left = journal_volume.find('(')
            bracket_right = journal_volume.find(')')
            journal_number = journal_volume[bracket_left + 1:bracket_right]  # "8-9"
            journal_volume = journal_volume[:bracket_left]  # "172"
            journal_vol_num = "T. " + str(journal_volume) + " — № " + str(journal_number)  # "T. 172 — № 8-9"
        else:
            journal_vol_num = "T. " + str(journal_volume)
    except:
        year_of_publication = ''
        journal_long = ''
        journal_vol_num = ''
        journal_pages = ''

    data = {'title': article_name,
            'year': year_of_publication,
            'authors': authors_string,
            'first_auth': authors_list,
            'journal': journal_long,
            'pages': journal_pages,
            'volume': journal_vol_num,
            'pmid': re.split('/', url_gen)[-1]}  # not the best way to get PMID from global URL_GEN

    # write_csv(data)
    generate_citation(data)


def main(pmid_list=["18234454", "14114836", "5660041", "6278869", "6290467", "bad_url"]):  # default value as an example
    pass  # заглушка для кода, оставил на память
    # Links are consist of two parts: "https://www.ncbi.nlm.nih.gov/pubmed/" + "18234454"
    base_url = "https://www.ncbi.nlm.nih.gov/pubmed/"

    counter = 0
    for item in pmid_list:
        counter += 1
        print(str(counter) + ' of ' + str(len(pmid_list)) + ': ' + str(item))  # just to visualise

        global url_gen
        url_gen = base_url + item
        html = get_html(url_gen)  # get html object

        if html.status_code == 200:  # if page is available - get data from html.text
            get_page_data(html.text)
        else:
            print('Page ' + url_gen + ' is not available. No link was generated.')

    return links  # returning list of links


if __name__ == '__main__':
    main()
