import numpy as np
import os
import nltk
import string
from nltk.corpus import abc
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer


# Lemmatize
wordnet_lemmatizer = WordNetLemmatizer()

def Lemmatize(sentence_tag):
    sentence_lemma = []
    for i in xrange(len(sentence_tag)):
        lem_list = []
        for each in sentence_tag[i]:
            word = each[0]
            tag = each[1]
            word = word.replace('&', '')
            word = filter(lambda x: x in printable, word)
            if tag[0] == 'V':
                lem_list.append(wordnet_lemmatizer.lemmatize(word, pos='v'))
            else:
                lem_list.append(wordnet_lemmatizer.lemmatize(word))
        sentence_lemma.append(lem_list)

    print sentence_lemma[0]
    return sentence_lemma



# Stemming
porter_stemmer = PorterStemmer()

def Stem(sentence_list):
    stem_list = []
    printable = set(string.printable)
    for i in xrange(len(sentence_list)):
        stem_lis = []
        for j in sentence_list[i]:
            stem_temp = j.replace('&','')
            stem_temp = filter(lambda x: x in printable, stem_temp)
            stem_lis.append(porter_stemmer.stem(stem_temp))
        stem_list.append(stem_lis)
    return stem_list


# Add Part_of_speech tag
def POS_Tagging(sentence_list):
    sentences_tag = []
    for each_sentence in sentence_list:
        sentence_tag_temp = nltk.pos_tag(each_sentence)
        sentences_tag.append(sentence_tag_temp)

    print sentences_tag[0]
    return sentences_tag


# Word Net
def Extract_Synset(sentence_list):
    hypernym = []
    hyponym = []
    holonym = []
    meronym = []

    for i in xrange(len(sentence_list)):
        hypernym_tmp = []
        hyponym_tmp = []
        holonym_tmp = []
        meronym_tmp = []
        for word in sentence_list[i]:
            if len(wn.synsets(word)) > 0:
                word_sense = wn.synsets(word)[0]
                ws_1 = word_sense.hypernyms()
                for j in ws_1:
                    hypernym_tmp += j.lemma_names()

                ws_2 = word_sense.hyponyms()
                for j in ws_2:
                    hyponym_tmp += j.lemma_names()

                ws_3 = word_sense.part_holonyms()
                for j in ws_3:
                    holonym_tmp += j.lemma_names()

                ws_4 = word_sense.part_meronyms()
                for j in ws_4:
                    meronym_tmp += j.lemma_names()

        hypernym.append(hypernym_tmp)
        hyponym.append(hyponym_tmp)
        holonym.append(holonym_tmp)
        meronym.append(meronym_tmp)

        # print hypernym_tmp
        # print hyponym_tmp
        # print holonym_tmp
        # print meronym_tmp

    return hypernym, hyponym, holonym, meronym



def Tag_XML(sentence_str, sentence_tag, sentence_stem, sentence_lem, sentence_list):
    hypernym, hyponym, holonym, meronym = Extract_Synset(sentence_list)
    open('./xml/task3.xml', 'w').close()
    with open('./xml/task3.xml', 'a') as file:
        file.writelines('<add>\n')
        for i in xrange(len(sentence_list)):
            print i
            file.writelines('<doc>\n')
            file.writelines('\t<field name=\"id\">' + str(i) + '</field>\n')
            file.writelines('\t<field name=\"name\">' + sentence_str[i] + '</field>\n')
            for j in sentence_list[i]:
                j = filter(lambda x: x in printable, j)
                file.writelines('\t<field name=\"word\">' + j.replace('&', '') + '</field>\n')
            # file.writelines('\t<field name=\"name\">' + sentences_str[i] + '</field>\n')
            for k in sentence_tag[i]:
                # j = filter(lambda x: x in printable, j)
                file.writelines('\t<field name=\"POS\">' + k[1] + '</field>\n')
            for each_stem in sentence_stem[i]:
                file.writelines('\t<field name=\"stem\">' + each_stem + '</field>\n')
            for each_lemma in sentence_lem[i]:
                file.writelines('\t<field name=\"lemma\">' + each_lemma + '</field>\n')

            for each_ws_1 in hypernym[i]:
                file.writelines('\t<field name=\"hypernym\">' + each_ws_1 + '</field>\n')
            for each_ws_2 in hyponym[i]:
                file.writelines('\t<field name=\"hyponym\">' + each_ws_2 + '</field>\n')
            for each_ws_3 in holonym[i]:
                file.writelines('\t<field name=\"holonym\">' + each_ws_3 + '</field>\n')
            for each_ws_4 in meronym[i]:
                file.writelines('\t<field name=\"meronym\">' + each_ws_4 + '</field>\n')

            file.writelines('</doc>\n')

        file.writelines('</add>')

if __name__ == '__main__':
    # Segment corpus into sentences and words
    sentences_list = abc.sents()
    # print sentences_list[0]
    printable = set(string.printable)
    sentences_str = []
    for i in xrange(len(sentences_list)):
        str_temp = " ".join(sentences_list[i])
        str_temp = str_temp.replace('&','')
        str_temp = filter(lambda x: x in printable, str_temp)
        sentences_str.append(str_temp)

    # stem_list = []
    stem_list = Stem(sentences_list)
    # print stem_list[0]
    sentences_tag = POS_Tagging(sentences_list)
    sentences_lemma = Lemmatize(sentences_tag)
    # print(sentences_lemma[4405])

    Tag_XML(sentences_str, sentences_tag, stem_list, sentences_lemma,sentences_list)