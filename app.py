import flask
from flask import request, jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/has_badword', methods=['post'])

def api_check_if_badword():
    import sys
    import csv

    # import pandas as pd 


    # try:
    #     from nltk import wordpunct_tokenize
    #     from nltk.corpus import stopwords
    # except ImportError:
    #     print ('[!] You need to install nltk (http://nltk.org/index.html)')

    # ------------read all bad words in dataset----------

    badwords_list=[]
    with open('english.csv') as f:
        lang_file = list(f.readlines())
    # print(lang_file)
    for i in range(0,len(lang_file)):
        coming_set=lang_file[i].replace("\n","").split(",")
        badwords_list.append(coming_set)
    # print(badwords_list)

    # -----convert to final list of the bad words
    def listToString(s): 
        str1=[]

        for ele in s: 
            for x in ele:
                str1.append(x)
                # print(x)
        return (str1)

    # print(listToString(badwords_list)) 

    badwords= listToString(badwords_list)


    # -----------------read test data-----------------

    request_data = request.get_json()

    # f = open("test-english.txt", "rt")
    testdata=request_data['message']



    #--------------- check for bad words-----------
    abuses=[]
    # x=[]
    # print("type of badwords_list : "+ str(type(badwords_list)))
    # print("type of testdata : "+ str(type(testdata)))
    # line_number=1
    testdata = testdata.split('\n')
    for sentence in testdata:
                # line_number = str(testdata.index(sentence)+1)
                for key in ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']:
                    sentence= sentence.replace(key,'')
                sentence=sentence.lower().split(" ")
            #     print(sentence)
                # print("type of sentence : "+ str(sentence))
                for i in sentence:
                    if i in badwords:
                        abuses.append(i)
                                    # print("i ="+ i)
                            # print("j ="+ str(j))
                if abuses == []:
                        isbadwords=False
                else:
                        isbadwords=True

    # if isbadwords==True:
    #     has_badword=["True"]
    # elif isbadwords==False:
    #     has_badword=["False"]
    # else:
    #     has_badword=["False"]
    # print("\n abuses: \n"+ str(abuses))
    # print("isbadword: ", isbadwords)
    return jsonify(hasbadword=isbadwords, inputdata=testdata)
app.run()

# print(api_check_if_badword())