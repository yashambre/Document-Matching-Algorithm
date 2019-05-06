
import os
import math
import nltk 
import codecs
from nltk.tokenize import RegexpTokenizer                 #imported RegexpTokenizer for tokenizing
from nltk.corpus import stopwords                         #imported stop_words to assign the stopwords in a list 
from nltk.stem.porter import PorterStemmer                #imported PortStemmer which is used for stemming tokens
from collections import Counter                           #imported Counter which is used to calculate term frequency



def getidf(token):                                       
	if any(x.isupper() for x in token):                  #isupper function checks if the query string has a uppercase   
		return -1.0000                                   #if its an uppercase word the result should be negative as it does  not take uppercase and lowercase as the same letter
	if token in DocFreq:
		return DocFreq[token]
	else:
		return -1.0000

def getqvec(qstring):                                    #Function with all the process such as tokenizing, stemming, stopwords, weights, 
	Qtoken_para=[]
	token = RegexpTokenizer(r'[a-zA-Z]+')
	Qtoken_para= token.tokenize(qstring.lower())
	#print (Qtoken_para)

	
	stop_words=list(set(stopwords.words('english')))
	Querystopw=[]
	for wor in Qtoken_para:
		if wor not in stop_words:
			Querystopw.append(wor)
	#print(Querystopw)

	

	QstemmedData=[]	
	Qstemmer = PorterStemmer()							 
	for s in Querystopw:										
		QstemmedData.append(Qstemmer.stem(s))
	#print(QstemmedData)

	QueryTOkF={}
	for wor in QstemmedData:
		QueryTOkF[wor] = 1 + math.log(QstemmedData.count(wor),10)
	#print(QueryTOkF)

	N = len(stemmedData)
	QueryDocFreq = {}
	for wor, freq in QueryTOkF.items():			                  #iterates 2D termFreqDict 
		freq = 0
		for para, t in TF.items():				                  #iterates inner dictionary
			if wor in TF[para].keys():						 #compares token in Dict					
				freq += 1						             #compares if token is present in termFreqDict i.e in every document								#if not,
			QueryDocFreq[wor] = math.log(N,10)               #if yes,increaments counter(Calculates document frequency)

		else:
			QueryDocFreq[wor] = math.log(N/freq,10)
	#print(QueryDocFreq)

	QueryWT={}
	for lett in QstemmedData:
			QueryWT[lett] = QueryTOkF[lett] * QueryDocFreq[lett] 					
	#print(QueryWT)

	sum=0
	for lett in QueryWT:					                    #Iterates through weights dictionary inorder to normalise the weight
		sum += QueryWT[lett] * QueryWT[lett] 					#Iterates inner Dict				
	for lett in QueryWT:
		QueryWT[lett] = QueryWT[lett]/math.sqrt(sum)
	

	return QueryWT

def query(query):                                            #Function to remove the Cosine similarity
	QueryWT = getqvec(query)
	#print(QueryWT)

	QuerySimilarity = {}

	for para in WT.keys():
		sum = 0
		for key, value in QueryWT.items():
			if key in WT[para].keys():
				sum += value * WT[para][key]
			else:
				sum += 0
		QuerySimilarity[para] = sum
	#print(QuerySimilarity)

	max_similarity_value = max(QuerySimilarity.values())
	max_similarity_value_key = max(QuerySimilarity, key = QuerySimilarity.get)
	if max_similarity_value == 0:
		return "NO MATCH\n", max_similarity_value
	else:
		return debate_transcript[max_similarity_value_key], max_similarity_value



#----------------------------------Stemming Words---------------------------------------------------

stop_words=list(set(stopwords.words('english')))			#assigns all stopwords to list stop_words
filename = './debate.txt'									#sets the path of files																
file = open (filename, "r", encoding='UTF-8') 				
doc = file.readlines()										#read all files in loop
file.close()                                                #closes all files in loop  


debate_transcript= {}                                      #Assingning A dictionary					
i = 1		
for k in doc:
	if not k.isspace():                                    #this returns the whole paragraph with the respected values
		debate_transcript["para " + str(i)] = k
		i+=1
#------------------------------------Tokenizing---------------------------------------------------

token_para=[]                                             
token = RegexpTokenizer(r'[a-zA-Z]+')                      #sets the tokenizing pattern that need to be filtered
for k in doc:
	if not k.isspace():                                    
		tok=[]
		tok= token.tokenize(k.lower())                     #tokenized
		token_para.append(tok)                             #appends the newly created list with all the tokens

#------------------------------------------Stopwords----------------------------------------------					
    
stop_words=list(set(stopwords.words('english')))          #assigns all stopwords to list stop_words
stopw=[]                                                  #defines a list
for wor in token_para:                                    #Two for loops are used to access the word inside the paragraph 
	temp=[]
	for token in wor:
		if token not in stop_words:                      
			temp.append(token)
	stopw.append(temp)                                    #it makes a list of tokens with all the words and without all the stopwords

#-----------------------------------------Stemming-------------------------------------------------------
stemmedData=[]	
stemmer = PorterStemmer()		                        #Stemmers remove morphological affixes from words, leaving only the word stem.					 
for s in stopw:										
	stem=[]
	for key in s:                                       #Stemming is create a list of words with only the stem of the words
		stem.append(stemmer.stem(key))
	stemmedData.append(stem)

# print(stemmedData)
#---------------------------------------------------Term Frequecy--------------------------------------

TF={}                                                  #term frequency is the number of  occurence of a particular word in a document
i=1
for lett in stemmedData:
	TOkF={}
	
	for wor in lett:
		TOkF[wor] = lett.count(wor)                  #Accesses the tokenized word in the dictionary
	
	for word,k in TOkF.items():                      #every element in the dictioanry has a key and value assign to it
		TOkF[word]= (math.log(k,10)+1)               #With the help of the value of each word we can calculate the term frequency
	TF["para " + str(i)] = TOkF                      #This line is done to name each paragraph with their following numbers 
	i+=1 					
#print(TF)

#-------------------------------------------------Document Frequency-------------------------------------------------

N= len(stemmedData)

DocFreq = {}
for FileName, tfDict in TF.items():			            #iterates 2D termFreqDict 
	for token, tf in tfDict.items():					#iterates inner dictionary
		counter = 0
		if token not in DocFreq:						#compares token in Dict
			for eachFileName, value in TF.items():
				if token in value:						#compares if token is present in term frequency i.e in every document
					counter += 1						#if yes,increaments counter(Calculates document frequency)
		if token not in DocFreq:						#if not, it calculates the document frequency
			DocFreq[token] = math.log(N/counter,10)
#print(DocFreq)


#--------------------------------------------------weigth----------------------------------------
WT={}                                                   #Calculates the weight of the document
B=1
for lett in TF:
	WTT={}
	for lor in TF[lett]:
		WTT[lor]=TF[lett][lor] * DocFreq[lor]         #Takes the document frequency and term frequency
	WT["para " + str(B)] = WTT
	B+=1 					
#print(WT)

#--------------------------------------------------Normalization--------------------------------------------


for document in WT:					                          #Iterates through weights dictionary inorder to normalise the weight
	sum=0
	for token,weight in WT[document].items():				#Iterates inner Dict
		sum += weight * weight 								#Next 4 steps performs normalisation
	for token2,weight2 in WT[document].items():
		WT[document][token2] = (weight2/math.sqrt(sum))
#print(WT)

