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
    
def printArticles(d):
    keys = list(d.keys())
    year = [d[x]['year'] for x in keys]

    sortedkeys = [x for (y,x) in sorted(zip(year,keys))][::-1]
 
    for key in sortedkeys:
        print('\\vbox{')
        print(formatAuthors(d[key]['author']), '\\\\')
        print(f'\\textit{{{d[key]["title"]}}} \\\\')
        print(d[key]['journal'])
        if('volume' in d[key]): 
            vstr = d[key]['volume']
            if('pages' in d[key]):
                vstr = vstr + ':' + d[key]['pages']
            print(vstr)
        if 'doi' in d[key]:
          doi_link = f'\\href{{https://doi.org/{d[key]["doi"]}}}{{\\color{{color1}}{{DOI link}}}}'
          print(doi_link)
        print('(' + d[key]['year'] + ')', '\\\\')
        print('}')
        print('')

#---------------------------------------------------------------------------

fname = 'citations.bib'

bibfile = open(fname,'r')
bp = BibTexParser(bibfile.read())
bibfile.close()

allarticles = bp.get_entry_dict()


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

print('\\section{First author peer-reviewed journal articles}', '\n')
printArticles(myarticles)
print('\\section{Last author peer-reviewed journal articles}', '\n')
printArticles(lastarticles)
print('\\section{Co-author peer-reviewed journal articles}', '\n')
printArticles(coarticles)
