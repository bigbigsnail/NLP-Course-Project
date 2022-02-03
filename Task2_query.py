from urllib2 import *
import json
import nltk
import os, sys
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

# main
if __name__ == '__main__':
    query = raw_input("Input query: ")

    q_sentences = sent_tokenize(query)
    for each_sentence in q_sentences:
        q_words = word_tokenize(each_sentence)

    # print(q_words)

    # Query input to SOLR
    q_solr = 'http://localhost:8983/solr/task3/select?q='
    q_solr = q_solr + q_words[0]
    for i in xrange(1,len(q_words)):
        q_solr = q_solr + '+' + q_words[i]
    q_solr = q_solr + '&wt=json&df=word&fl=id,name'
    print(q_solr)

    connection = urlopen(q_solr)
    response = json.load(connection)

    print response['response']['numFound'], "documents found."

    for document in response['response']['docs']:
        print " Id, Name =", document['id'],"\t", document['name']