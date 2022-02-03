# import abc corpora from nltk
from nltk.corpus import abc
import string

# Segment the corpus into sentences and words
sentences_list = abc.sents()
words = abc.words()

# Show the number of sentences and words in the corpus
print len(sentences_list)
print len(words)

printable = set(string.printable)
sentences_str = []
for i in xrange(len(sentences_list)):
    str_temp = " ".join(sentences_list[i])
    str_temp = str_temp.replace('&','')
    str_temp = filter(lambda x: x in printable, str_temp)
    sentences_str.append(str_temp)
print sentences_str[0]
print sentences_list[0][:]

# print(sentences_str[4405])
# print(sentences_str[4406])

open('./xml/task1.xml', 'w').close()
with open('./xml/task1.xml', 'a') as file:
    file.writelines('<add>\n')

    for i in xrange(len(sentences_str)):
        # print i
        file.writelines('<doc>\n')
        file.writelines('\t<field name=\"id\">' + str(i) + '</field>\n')
        file.writelines('\t<field name=\"name\">' + sentences_str[i] + '</field>\n')
        for j in sentences_list[i]:
            j = filter(lambda x: x in printable, j)
            file.writelines('\t<field name=\"word\">'+j.replace('&','') +'</field>\n')
        file.writelines('</doc>\n')

    file.writelines('</add>')