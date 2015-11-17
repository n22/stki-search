import xlwt
import xlrd
from xlutils.copy import copy
import re, collections

class excel:
    def __init__(self):
        pass

    def readExcel(self,filePath):
        excel = xlrd.open_workbook(filename=filePath)
        dicts = excel.sheet_by_index(0)
        return dicts

class synonim(excel):

    def __init__(self):
        pass

    def getSynonim(self,inp):
        dicts = excel.readExcel(self,'synonim.xlsx')
        for x in range(0,dicts.nrows):
            itr = 0
            for idx,cell_obj in enumerate(dicts.row(x)):
                if (itr == 0 ):
                    key = str.lower(str(cell_obj.value))
                if (str.lower(str(cell_obj.value)) == str.lower(str(inp))):
                    return key
                itr+=1
        return inp
if __name__ == '__main__':
    def words(text): return re.findall('[a-z]+', text.lower()) 
    def train(features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model
     
    NWORDS = train(words(file('big.txt').read()))
     
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
     
    def edits1(word):
        n = len(word)
        return set([word[0:i]+word[i+1:] for i in range(n)] +                     # deletion
                   [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + # transposition
                   [word[0:i]+c+word[i+1:] for i in range(n) for c in alphabet] + # alteration
                   [word[0:i]+c+word[i:] for i in range(n+1) for c in alphabet])  # insertion
     
    def known_edits2(word):
        return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)
     
    def known(words): 
      return set(w for w in words if w in NWORDS)
     
    def correct(word):
        candidates = known([word]) or known(edits1(word)) or known_edits2(word) or [word]
        return max(candidates, key=lambda w: NWORDS[w])
    s = ' '.join(correct(word) for word in words(raw_input('Give sentence: ')))
    print s
    synm = synonim()
    print synm.getSynonim(s)