import glob
import sys, os
import time
from Text_Extractor import PDF_Reader,Docx_Reader,txt_Reader
from DB_File import create_db,insert_values_into_files_path,insert_values_into_word_path,\
					insert_values_into_file_time_stamps

# we are taking the bigrams and trigrams
def convert_2_Bi_trigrams(word_list):
	bigrams,trigrams = [],[]
	for i in range(len(word_list)-2):
		val = word_list[i] + ' ' + word_list[i+1]
		bigrams.append(val)
	for i in range(len(word_list)-3):
		val = word_list[i] + ' ' + word_list[i+1] + ' ' +word_list[i+2]
		trigrams.append(val)	

	return bigrams+trigrams


if __name__ == '__main__':


	Path_list = []

	rootdir = input("Enter folder to be searched: ")
	rootdir += "/"

	# we are obtaining the files in the directory and subdirectories 
	for path in glob.glob(f'{rootdir}**/*',recursive = True):
		split_tup = os.path.splitext(path)
		print(path)
		if split_tup[1] == '.docx' or split_tup[1]== '.pdf' or split_tup[1] == '.txt':
			Path_list.append(path)


	create_db()# creates tables

	# Processing the PDF files 
	for path in Path_list:
		split_tup = os.path.splitext(path)
		file_name = split_tup[0].split("/")[-1]
		if split_tup[1]== '.pdf':
			time_stamp = os.path.getctime(path)
			insert_values_into_files_path((file_name.lower(),path))# Pushing the file name and path into the DB
			insert_values_into_files_path(('.pdf',path))# Pushing type of the file and path into DB
			insert_values_into_file_time_stamps((file_name.lower(),path,time_stamp))# Pusing the file and time stamps(created time)
			word_list = PDF_Reader(path)
			word_list += convert_2_Bi_trigrams(word_list)
			for word in word_list:
				insert_values_into_word_path((word,path)) #Inserting the words(bigrams+trigrams) into the DB


	for path in Path_list:
		split_tup = os.path.splitext(path)
		file_name = split_tup[0].split("/")[-1]
		if split_tup[1]== '.docx':
			time_stamp = os.path.getctime(path)
			insert_values_into_files_path((file_name.lower(),path))# Pushing the file name and path into the DB
			insert_values_into_files_path(('.docx',path))# Pushing type of the file and path into DB
			insert_values_into_file_time_stamps((file_name.lower(),path,time_stamp))# Pusing the file and time stamps(created time)
			word_list = Docx_Reader(path)
			word_list += convert_2_Bi_trigrams(word_list)

			for word in word_list:
				insert_values_into_word_path((word,path))#Inserting the words(bigrams+trigrams) into the DB

	for path in Path_list:
		split_tup = os.path.splitext(path)
		file_name = split_tup[0].split("/")[-1]
		if split_tup[1]== '.txt':
			time_stamp = os.path.getctime(path)
			insert_values_into_files_path((file_name.lower(),path))# Pushing the file name and path into the DB
			insert_values_into_files_path(('.txt',path))# Pushing type of the file and path into DB
			insert_values_into_file_time_stamps((file_name.lower(),path,time_stamp))# Pusing the file and time stamps(created time)
			word_list = txt_Reader(path)
			word_list += convert_2_Bi_trigrams(word_list)

			for word in word_list:
				insert_values_into_word_path((word,path))#Inserting the words(bigrams+trigrams) into the DB




