import flask
from flask import request, jsonify
import csv
import os.path


app = flask.Flask(__name__)
app.config["DEBUG"] = True


#--------------- CHECK BADWORD API----------------------

@app.route('/api/has_badword', methods=['post'])

def api_check_if_badword():

    request_data = request.get_json()
    languages=request_data['languages']
    in_comment=request_data['message'].encode('utf-8')

    def listToString(s):
        str1=[]
        for ele in s:
            for x in ele:
                str1.append(x)
                # print(x)
        return (str1)

    isbadwords="false"
    is_valid_lang="true"
    invalid_lang=[]

    for lang in languages:
    	if os.path.exists(lang.lower()+'.csv')==True:
    		badwords_list=[]
    		with open(lang.lower()+'.csv', "rb") as f:
        		lang_file = list(f.readlines())
        	f.close()
    #except Exception as e:
     #   print("\nerror occured " + str(e))

        	for i in range(0,len(lang_file)):
            		coming_set=lang_file[i].replace("\r","").replace("\n","").split(",")
            		badwords_list.append(coming_set)
    		badwords= listToString(badwords_list)

    #--------------- check for bad words-----------
        	abuses=[]

     		comment = in_comment.split('\n')
     		for sentence in comment:
                	for key in ['.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}']:
                    		sentence= sentence.replace(key,'')
                	sentence=sentence.lower()
                	for i in badwords:
                    		if i in sentence:
                        		abuses.append(i)

                	if abuses == []:
                        	print("\nno bad words for "+ str(lang).upper()+ " language")
                	else:
                        	isbadwords="true"
				print("\nbadwords detected for " +str(lang).upper()+ " language")

	else:
		print("\nLanguage not supported: "+ lang.upper())
		is_valid_lang="false"
		invalid_lang.append(lang)

    if isbadwords=="true":
         print("\nBad words detected")
	 #print(abuses)
    else:
	 print("\n\nNo bad word in comment")
    return jsonify(hasbadword=isbadwords, is_valid_lang=is_valid_lang, invalid_lang=invalid_lang)


#-------------------LIST BADWORD API------------



@app.route('/api/list_badwords', methods=['get'])

def list_badwords():

	request_data = request.get_json()
	lang=request_data['language']

	badwords_list=[]
	badwords=[]
	is_valid_lang="false"
	if os.path.exists(lang.lower()+'.csv')==True:
		is_valid_lang="true"
		with open(lang.lower()+'.csv',"rb") as f:
        		lang_file = list(f.readlines())

		f.close()
    # print(lang_file)
		for i in range(0,len(lang_file)):
        		coming_set=lang_file[i].replace("\r","").replace("\n","").split(",")
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
	    	print("\nListing all bad words for "+ lang.upper() )

	else:
		print("\n Language file not found for "+ lang.upper())
		is_valid_lang="false"

	return jsonify(badwords_list=badwords, is_valid_lang=is_valid_lang)



#-------------ADD BADWORD API---------------


@app.route('/api/add_badwords', methods=['post'])

def add_badwords():

	request_data = request.get_json()

    # f = open("test-english.txt", "rt")
	add_data=request_data['addword']
	lang=request_data['language']
    #print (str(add_data))
	is_lang_valid="false"
	if os.path.exists(lang.lower()+'.csv')==True:
		is_lang_valid="true"
		with open(lang.lower()+'.csv', 'a') as f_object:
			writer_object=csv.writer(f_object)
			alist=[]
			words_added=[]
			for i in add_data:
				alist.append(i)
				writer_object.writerow(alist)
				print("Added " + i +" to bad word list")
				alist=[]
				words_added.append(i)
		is_word_added="true"
		#words_added=alist
		f_object.close()
	else:
		is_lang_valid="false"
		print("\nLanguage file not found for " + lang.upper())
		is_word_added="false"
		words_added=[]

	return jsonify(is_lang_valid=is_lang_valid, is_word_added=is_word_added, words_added= words_added)



#-----------------DELETE BADWORD API---------------
@app.route('/api/delete_badwords', methods=['post'])

def delete_badwords():

	request_data=request.get_json()
	delete_data=request_data['deletewords']
	lang=request_data['language']

	lines=list()
	badword_inlist="false"
	deleted_words=[]

	data_to_delete=[]
	for j in delete_data:
		data_to_delete.append(j.encode('utf-8'))


	is_valid_lang="false"
	if os.path.exists(lang.lower()+'.csv')==True:
		is_valid_lang="true"
		with open(lang.lower()+ '.csv', 'r') as readFile:
			reader=csv.reader(readFile)
			for row in reader:
				#for i in row:
				lines.append(row)
#			lines=reader
#		print("\nUpdated lines list\n")
#		print(lines)
		flines=[]
		for row in lines:
			flines.append(row)
		for i in lines:
			#print("\n--------this is i--------"+ str(i))
			for j in i:
			#	print("\ni= " + str(i))
			#	print("\nj= "+ str(j))
				if j in data_to_delete:
			#		print("\n---match-------"+ j)
					flines.remove(i)
			#		print("\n----------updated flines--"+ str(flines))
					badword_inlist="true"
					deleted_words.append(j)
					print("Deleted "+ j + " from "+ lang.upper() )


		#print("\nData to delete \n")
		#print(data_to_delete)
			#print(lines)
		readFile.close()


		with open(lang.lower()+'.csv','w') as writeFile:
			writer=csv.writer(writeFile)
			writer.writerows(flines)
		writeFile.close()

	else:
		print("\nLanguage file not found for " + lang)
		is_valid_lang="false"
		deleted_words=[]

	return jsonify(is_valid_lang=is_valid_lang, is_word_deleted=badword_inlist, words_deleted = deleted_words)



#--------------- ADD BADWORD API (LANG)----------------------

@app.route('/api/add_badword_lang', methods=['post'])

def add_badword_lang():


	request_data = request.get_json()
	language=request_data['language'].encode('utf-8')
	badwords=request_data['addwords']
	newFile=open(language.lower()+'.csv',"w")
	print("file created")

	writer=csv.writer(newFile)
	#writer.writerows([s for s in badwords])

	alist=[]
	for i in badwords:
		alist.append(i.encode('utf-8'))
		writer.writerow(alist)
		print("Added " + i +" to bad word list")
		alist=[]


	print("bad words added")
	newFile.close()

	badwords_list=[]
 	with open(language.lower()+'.csv') as f:
        	lang_file = list(f.readlines())
    # print(lang_file)
	for i in range(0,len(lang_file)):
		coming_set=lang_file[i].replace("\r","").replace("\n","").split(",")
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
	print("Listing all bad words")



    	return jsonify(lang=language, words=badwords) #str(type(language)) #jsonify(type= type(language))





app.run()
