from bibtexparser.bparser import BibTexParser
import unicodedata

def convertStr(string):
    if type(string) != str: uni = string.decode('unicode-escape')
    else: uni = string

    return unicodedata.normalize('NFKD',uni).encode('ascii','ignore')

def formatAuthors(s):
    ss  = s.split(' and ')
    others = False
    while 'others' in ss: 
        ss.remove('others')
        others = True
    while 'Others' in ss: 
        ss.remove('Others')
        others = True
    sss = [x.split(', ')[1][0] + ' ' + x.split(', ')[0] for x in ss]
    sss = ', '.join(sss)

    if(others): sss = sss + ' et al.'

    return sss
    
def printArticles(d, f):
    keys = list(d.keys())
    year = [d[x]['year'] for x in keys]

    sortedkeys = [x for (y,x) in sorted(zip(year,keys))][::-1]
 
    for key in sortedkeys:
        print('\\vbox{', file = f)
        print(formatAuthors(d[key]['author']), '\\\\', file = f)
        print(f'\\textit{{{d[key]["title"]}}} \\\\', file = f)
        print(d[key]['journal'], file = f)
        if('volume' in d[key]): 
            vstr = d[key]['volume']
            if('pages' in d[key]):
                vstr = vstr + ':' + d[key]['pages']
            print(vstr, file = f)
        if 'doi' in d[key]:
          doi_link = f'\\href{{https://doi.org/{d[key]["doi"]}}}{{\\color{{color1}}{{DOI link}}}}'
          print(doi_link, file = f)
        print('(' + d[key]['year'] + ')', '\\\\', file = f)
        print('} \\smallskip', file = f)
        print('', file = f)

def printProceedings(d, f):
    keys = list(d.keys())
    year = [d[x]['year'] for x in keys]

    sortedkeys = [x for (y,x) in sorted(zip(year,keys))][::-1]
 
    for key in sortedkeys:
        if 'conference' in d[key]:
          print('\\vbox{', file = f)
          print(formatAuthors(d[key]['author']), '\\\\', file = f)
          print(f'\\textit{{{d[key]["title"]}}} \\\\', file = f)
          print(d[key]['conference'], file = f)
          if 'doi' in d[key]:
            doi_link = f'\\href{{https://doi.org/{d[key]["doi"]}}}{{\\color{{color1}}{{DOI link}}}}'
            print(doi_link, file = f)
          print('(' + d[key]['year'] + ')', '\\\\', file = f)
          print('} \\smallskip', file = f)
          print('', file = f)

#---------------------------------------------------------------------------

# read all articles
with open('articles.bib','r') as bibfile:
  bp = BibTexParser(bibfile.read())
allarticles = bp.get_entry_dict()

# split articles into first, last, co-author
myarticles = {}
lastarticles = {}
coarticles = {}

for x in list(allarticles.keys()): 
  if allarticles[x]['ENTRYTYPE'] == 'article':
    all_authors = [x.strip() for x in allarticles[x]['author'].split('and')]
    if all_authors[0].startswith('Schramm'): 
      myarticles[x] = allarticles[x]
    elif all_authors[-1].startswith('Schramm'): 
      lastarticles[x] = allarticles[x]
    else: 
      coarticles[x] = allarticles[x]

# read all proceedings
with open('proceedings.bib','r') as bibfile:
  bpc = BibTexParser(bibfile.read())
allprocs = bpc.get_entry_dict()

with open('publications_gs.tex', 'w') as f:
  print('\\section{First author peer-reviewed journal articles}', '\n', file = f)
  printArticles(myarticles, f)
  print('\\section{Last author peer-reviewed journal articles}', '\n', file = f)
  printArticles(lastarticles, f)
  print('\\section{Co-author peer-reviewed journal articles}', '\n', file = f)
  printArticles(coarticles, f)
  print('\\section{Conference proceedings}', '\n', file = f)
  printProceedings(allprocs, f)
