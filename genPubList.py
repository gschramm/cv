import urllib.request
import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import *

def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = type(record)
    record = homogenize_latex_encoding(record)
    record = author(record)
    record = editor(record)
    record = journal(record)
    record = keyword(record)
    record = link(record)
    record = page_double_hyphen(record)
    record = doi(record)
    return record

def format_author_list(author_list: list[str]) -> str:
    return ', '.join([f'{x.split(", ")[1]} {x.split(", ")[0]}' for x in author_list])

def printArticles(entry_list, f):
    for d in entry_list:
        print('\\vbox{', file = f)
        print(format_author_list(d['author']), '\\\\', file = f)
        title = d['title'].replace('\gamma','$\gamma$')
        print(f'\\textit{{{title}}} \\\\', file = f)
        print(d['journal']['name'], file = f)
        if('volume' in d): 
            vstr = d['volume']
            if('pages' in d):
                vstr = vstr + ':' + d['pages']
            print(vstr, file = f)
        if 'doi' in d:
          doi_link = f'\\href{{https://doi.org/{d["doi"]}}}{{\\color{{color1}}{{DOI link}}}}'
          print(doi_link, file = f)
        print('(' + d['year'] + ')', '\\\\', file = f)
        print('} \\smallskip', file = f)
        print('', file = f)


def printProceedings(entry_list, f):
    for d in entry_list:
        if 'conference' in d:
            print('\\vbox{', file = f)
            print(format_author_list(d['author']), '\\\\', file = f)
            print(f'\\textit{{{d["title"]}}} \\\\', file = f)
            print(d['conference'], file = f)
            if 'doi' in d:
                doi_link = f'\\href{{https://doi.org/{d["doi"]}}}{{\\color{{color1}}{{DOI link}}}}'
                print(doi_link, file = f)
            print('(' + d['year'] + ')', '\\\\', file = f)
            print('} \\smallskip', file = f)
            print('', file = f)


#-------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # download bibtex file of articles
    urllib.request.urlretrieve('https://raw.githubusercontent.com/gschramm/gschramm.github.io/master/_bibliography/papers.bib', 'articles.bib')

    with open('articles.bib', 'r') as bibtex_file:
        parser = BibTexParser()
        parser.customization = customizations
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
    
        first_author_entries = []
        last_author_entries = []
        co_author_entries = []
    
        for x in bib_database.entries:
            if x['author'][0].startswith('Schramm, G'):
                first_author_entries.append(x)
            elif x['author'][-1].startswith('Schramm, G'):
                last_author_entries.append(x)
            else:
                co_author_entries.append(x)

    with open('proceedings.bib', 'r') as bibtex_file:
        parser = BibTexParser()
        parser.customization = customizations
        proc_database = bibtexparser.load(bibtex_file, parser=parser)
    
    with open('publications_gs.tex', 'w') as f:
        print('\\section{First author peer-reviewed journal articles}', '\n', file = f)
        printArticles(first_author_entries, f)
        print('\\section{Last author peer-reviewed journal articles}', '\n', file = f)
        printArticles(last_author_entries, f)
        print('\\section{Co-author peer-reviewed journal articles}', '\n', file = f)
        printArticles(co_author_entries, f)
        print('\\section{Conference proceedings}', '\n', file = f)
        printProceedings(proc_database.entries, f)
