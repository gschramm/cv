import urllib3
import pylab      as py
import datetime

tablePattern = '"gsc_rsb_std">'
plotPattern  = '"gsc_g_al">'

yearlyCitations = []
years           = []

url   = 'https://scholar.google.de/citations?user=_txZ90cAAAAJ&hl=de&oi=ao'  
http  = urllib3.PoolManager() 
lines = str(http.request('GET',url).data)

pstr      = lines.split(plotPattern)[1:]
citations = [ int(x.split('</span>')[0]) for x in pstr ]

ystr  = lines.split('<span class="gsc_g_t"')[1:]
years = [ int(x[x.find('>') + len('>'):x.find('<')]) for x in ystr ]

tstr  = lines.split(tablePattern)[1:]
h     = [ int(x.split('</td>')[0]) for x in tstr ]

numOfCitations       = h[0]
numOfCitationsLast10 = h[1]

hIndex       = h[2]
hIndexLast10 = h[3]

i10Index       = h[4]
i10IndexLast10 = h[5]

q = lines.split('class="gs_gray"')

titles     = []
authors    = []
journals   = []
ncitations = []

print('\n\n-------------------')
print('Most cited articles')
print('-------------------')

for i in range(int(len(q)/2)):
  x = q[2*i]
  y = q[2*i + 1]
  z = q[2*i + 2]
  titles.append(x[(x.rfind('class="gsc_a_at">') + len('class="gsc_a_at">')):x.rfind('</a><div')])
  authors.append(y[y.find('>') + len('>'):y.find('<')])
  journals.append(z[z.find('>') + len('>'):z.find('<')])
  ncitations.append(int(z[(z.find('class="gsc_a_ac gs_ibl">') + 
                          len('class="gsc_a_ac gs_ibl">')):z.find('</a>')]))

  print('')
  print(i+1)
  print(authors[-1])
  print(titles[-1])
  print(journals[-1])
  print('num of citations: ', ncitations[-1])

fig, ax = py.subplots(figsize = (4,2.5))

p1 = ax.bar(years,citations)
ax.set_ylabel('citations per year')

now = datetime.datetime.now()
hstr = 'Google scholar' + ' - date: ' + str(now.date()) + '\ntotal citations: ' + str(numOfCitations) + ' - h index: ' + str(hIndex) 

ax.set_title(hstr, fontsize = 'small')
py.tight_layout()

ax.set_axisbelow(True)
ax.grid(ls='--')

fig.savefig('citationMetrics.pgf')    

py.show()
