from urllib2 import *
import json
import nltk
import os, sys
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()
porter_stemmer = PorterStemmer()

# main
if __name__ == '__main__':
    query = raw_input("Input query: ")
    # search_field = raw_input("Input search field: ")
    q_sentences = sent_tokenize(query)
    for each_sentence in q_sentences:
        q_words = word_tokenize(each_sentence)

    q_pos_tag = nltk.pos_tag(q_words)
    q_lemma = []
    q_stem = []
    q_hyper = []
    # q_hypo = []
    # q_holo = []
    # q_mero = []
    for each in q_pos_tag:
        word = each[0]
        tag = each[1]
        if tag[0] == 'V':
            q_lemma.append(wordnet_lemmatizer.lemmatize(word, pos='v'))
        else:
            q_lemma.append(wordnet_lemmatizer.lemmatize(word))
    for each in q_words:
        q_stem.append(porter_stemmer.stem(each))
    for each in q_words:
        if len(wn.synsets(word)) > 0:
            word_sense = wn.synsets(word)[0]
            ws_1 = word_sense.hypernyms()
            for j in ws_1:
                q_hyper += j.lemma_names()
            '''
            ws_2 = word_sense.hyponyms()
            for j in ws_2:
                q_hypo += j.lemma_names()
                
            ws_3 = word_sense.part_holonyms()
            for j in ws_3:
                q_holo += j.lemma_names()

            ws_4 = word_sense.part_meronyms()
            for j in ws_4:
                q_mero += j.lemma_names()
            '''
    print(q_words)
    print(q_pos_tag)
    print(q_lemma)
    print(q_stem)
    print(q_hyper)
    # print(q_hypo)
    # print(q_holo)
    # print(q_mero)


    # Query input to SOLR
    q_solr = 'http://localhost:8983/solr/task3/select?q=stem:'
    q_solr = q_solr + q_stem[0]
    for i in xrange(1, len(q_stem)):
        q_solr = q_solr + '+' + q_stem[i]
    q_solr = q_solr + '%20lemma:'
    q_solr = q_solr + q_lemma[0]
    for i in xrange(1, len(q_lemma)):
        q_solr = q_solr + '+' + q_lemma[i]
    q_solr = q_solr + '%20hypernym:'
    q_solr = q_solr + q_hyper[0]
    for i in xrange(1, len(q_hyper)):
        q_solr = q_solr + '+' + q_hyper[i]
    q_solr = q_solr + '&wt=json&fl=id,name'
    print(q_solr)

    connection = urlopen(q_solr)
    response = json.load(connection)

    print response['response']['numFound'], "documents found."

    for document in response['response']['docs']:
        print " Id, Name =", document['id'],"\t", document['name']