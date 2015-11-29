__author__ = 'hamdiahmadi'

import pymysql
import xlwt
import xlrd
from xlutils.copy import copy
import re, collections
import copy

class excel():
    def __init__(self):
        pass

    def readExcel(self,filePath):
        excel = xlrd.open_workbook(filename=filePath)
        dicts = excel.sheet_by_index(0)
        return dicts

class query():
    def __init__(self):
        pass

    def openingConnection(self,addrs,users,passwords,dbNames):
        return pymysql.connect(passwd=passwords,db=dbNames,host=addrs,user=users)

    def executing(self,cursor,command):
        return cursor.execute(command)

    def closingConnection(self,cursor):
        return cursor.close()

    def fetchingAll(self,cursor):
        return cursor.fetchall()

    def getQuery(self,words,addr,user,password,dbName):
        db = self.openingConnection(addr,user,password,dbName)
        query_from = []
        query_where = []
        cursor = db.cursor()
        for word in words.split():
            sql = 'select *,count(*) as cnt from dictionary where keyword like "' +word+ '" group by table_source,column_source order by cnt desc'
            self.executing(cursor,sql)
            res = self.fetchingAll(cursor)
            for y in res:
                print y
        query = ''
        return query

class autoCorrect():

    def __init__(self):
        self.NWORDS = self.train(self.words(file('big.txt').read()))
        self.alphabet = 'abcdefghijklmnopqrstuvwxyz'

    def words(self,text):
        return re.findall('[a-z,0-9]+', text.lower())
    def train(self,features):
        model = collections.defaultdict(lambda: 1)
        for f in features:
            model[f] += 1
        return model

    def edits1(self,word):
        n = len(word)
        return set([word[0:i]+word[i+1:] for i in range(n)] +                     # deletion
                   [word[0:i]+word[i+1]+word[i]+word[i+2:] for i in range(n-1)] + # transposition
                   [word[0:i]+c+word[i+1:] for i in range(n) for c in self.alphabet] + # alteration
                   [word[0:i]+c+word[i:] for i in range(n+1) for c in self.alphabet])  # insertion

    def known_edits2(self,word):
        return set(e2 for e1 in self.edits1(word) for e2 in self.edits1(e1) if e2 in self.NWORDS)

    def known(self,words):
      return set(w for w in words if w in self.NWORDS)

    def correct(self,word):
        try:
            int(word)
            return word
        except:
            pass
        candidates = self.known([word]) or self.known(self.edits1(word)) or self.known_edits2(word) or [word]
        return max(candidates, key=lambda w: self.NWORDS[w])

    def getAutoCorrect(self,word_input):
        s = ' '.join(self.correct(word) for word in self.words(word_input))
        return s

class synonim(excel,query):
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

class trie(excel):
    def __init__(self):
        pass

    def makeArray(self):
        return [[[-1,''] for x in range(255)] for x in range(1000)]

    def insertTrie(self):
        dicts = dict()
        content = excel.readExcel(self,'synonim.xlsx')
        for x in range(0,content.nrows):
            itr = 0
            for idx,cell_obj in enumerate(content.row(x)):
                if cell_obj.value == '':
                    break
                if itr == 0:
                    return_value = copy.copy(cell_obj.value)
                else :
                    word = ''
                    tmp = dicts
                    lists = (cell_obj.value).split(' ')
                    for w in range(0,len(lists)):
                        lists[w] = str.lower(str(lists[w]))
                        if w == 0:
                            word = lists[w]
                        else:
                            word = word+' '+lists[w]
                        try:
                            try:
                                if w == len(lists)-1 :
                                    tmp[lists[w]][1] = copy.copy(return_value)
                                else :
                                    tmp = tmp[lists[w]][0]
                            except:
                                tmp = tmp[lists[w]][0]
                        except:
                            if w == len(lists)-1 :
                                tmp[lists[w]] = [dict(),copy.copy(return_value)]
                            else :
                                tmp[lists[w]] = [dict(),copy.copy(word)]
                                tmp = tmp[lists[w]][0]
                itr+=1
        return dicts

    def addingSynonim(self,word):
        content = excel.readExcel(self,'synonim.xlsx')
        word = str.lower(str(word))
        res = word
        for x in range(0,content.nrows):
            itr = 0
            if str.lower(str(content.row(x)[0].value)) == word:
                for idx,cell_obj in enumerate(content.row(x)):
                    if itr == 0:
                        pass
                    else :
                        res = res +' '+str.lower(str(cell_obj.value))
                    itr+=1
                return res
        return res

    def deleteRedundance(self,word):
        dicts = dict()
        res = ''
        for x in word.split():
            try :
                if (dicts[x] == 1):
                    pass
            except :
                dicts[x] = 1
                if res == '':
                    res = x
                else:
                    res = res +' '+x
        return res

    def searchTrie(self,words):
        lists = words.split(' ')
        tries = self.insertTrie()
        res = ''
        sen = ''
        x = 0
        while x <= len(lists)-1:
            dictionary = tries
            lists[x] = str.lower(str(lists[x]))
            sen = lists[x]
            for y in range(x,len(lists)):
                try:
                    sen = dictionary[lists[y]][1]
                    dictionary = dictionary[lists[y]][0]
                    if y == len(lists)-1 and res == '':
                        # res = sen
                        res = self.addingSynonim(sen)
                        x=y+1
                    elif y == len(lists)-1:
                        # res = res + ' ' + sen
                        res = res + ' ' + self.addingSynonim(sen)
                        x=y+1
                except:
                    if res == '':
                        res = sen
                    else :
                        # res = res + ' ' + sen
                        res = res + ' ' + self.addingSynonim(sen)
                    if (x!=y):
                        x=y
                    else :
                        x=y+1
                    break
        res = self.deleteRedundance(res)
        return res

class tolerance(synonim,autoCorrect,query,trie):

    def __init__(self):
        autoCorrect.__init__(self)

    def getTolerance(self,words):
        addr = "128.199.181.164"
        user = "stki"
        password = "stki2015"
        dbName = "stki"
        # words = autoCorrect.getAutoCorrect(self,words)
        return trie.searchTrie(self,words)
        # return query.getQuery(self,words,addr,user,password,dbName)

if __name__ == '__main__':
    q = tolerance()
    print q.getTolerance(raw_input('Give sentence: '))
