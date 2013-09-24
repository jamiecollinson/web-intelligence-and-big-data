#!/usr/bin/env python
import glob, mincemeat, pickle

text_files = glob.glob('hw3data/*')

data = []
for file in text_files:
  for line in open(file).readlines():
    data.append(line)
        
def mapfn(k, v):
    from stopwords import allStopWords as stopwords 
    stopwords = stopwords.keys()
    publication, authors, title = v.split(':::')
    for author in authors.split('::'):
      for word in title.split(' '):
        if (word not in stopwords and len(word) > 1):
          yield (author, filter(str.isalnum, word)), 1

def reducefn(k, vs):
    result = 0
    for v in vs:
        result += v
    return result

try:
  results = pickle.load( open("results.p", "rb") )
except:
  s = mincemeat.Server()
  
  s.datasource = dict(enumerate(data))
  s.mapfn = mapfn
  s.reducefn = reducefn
  
  results = s.run_server(password="changeme")

  pickle.dump(results, open("results.p", "wb"))
  
print "complete"
while True:
  search = raw_input('name to search: ')
  for key in results.keys():
    if key[0].startswith(search):
      print key, results[key]