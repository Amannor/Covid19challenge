import os
import sys
import json
import gzip
import datetime

start_time = datetime.datetime.now()
overall_files_count = 0
skipped_files_count = 0
#Init the set of articles ids
ids_file_path = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\nonempty_ids_of_full_text_articles.txt'
ids = set()
with open(ids_file_path) as infile:
    for line in infile:
        if line:
        	ids.update(map(str.strip, line.split(";")))


## Configurations
#ORIGINAL: data_path = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\CORD-19-research-challenge\noncomm_use_subset\noncomm_use_subset\pmc_json'
data_paths = [r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\biorxiv_medrxiv\biorxiv_medrxiv\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pmc_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pmc_json',r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pmc_json']

def is_paper_id_in_ids(raw_id):
	cur_ids = map(str.strip, raw_id.split(";"))
	cur_ids = list(filter(lambda x: x in ids, cur_ids))
	return len(cur_ids)>0

amount_of_files_to_use = 1000
root_file_initialized = False
def extract_text(file_path):
    with open(file_path, 'r') as f:
        cur_file_as_dict = json.load(f)
    list_of_texts = cur_file_as_dict['body_text']
    full_text = ''
    if(is_paper_id_in_ids(cur_file_as_dict['paper_id'])):
    	full_text = ' '.join([lof['text'] for lof in list_of_texts])
    return full_text

for data_path in data_paths:
	## Extracting the text
	files_found = [f for f in os.listdir(data_path) if f.endswith('.json')]
	files_found_full_path = [os.path.join(data_path, f) for f in files_found]
	files_path_subset = files_found_full_path[0:len(files_found)]#files_found_full_path[0:amount_of_files_to_use]
	# print(f"{len(files_found)} files have been found, we will use the top {len(files_found)} as set in the configuration")

	## Comparing between pairs of documents
	# first_document_idx = 0
	# second_document_idx = 1

	if(not root_file_initialized):
		first_document_idx = 0
		first_file = files_path_subset[first_document_idx]
		first_text = extract_text(first_file)
		while(first_document_idx<len(files_path_subset) and not first_text):
			first_document_idx = first_document_idx+1
			first_file = files_path_subset[first_document_idx]
			first_text = extract_text(first_file)
		
		print(f"first_file {first_file} first_document_idx {first_document_idx}")		
		zipped_first_text = gzip.compress(bytes(first_text,'utf-8'))
		print(f"Length of the zipped first document {len(zipped_first_text)}")
		print(f"First document compression substraction result: {len(bytes(first_text, 'utf-8')) - len(zipped_first_text)}")

	root_file_initialized = True
	# print(f"Length of the first document {len(bytes(first_text, 'utf-8'))}")
	overall_files_count = overall_files_count+len(files_path_subset)
	for second_document_idx in range(first_document_idx+1, len(files_path_subset)):
	
		second_file = files_path_subset[second_document_idx]
		second_text = extract_text(second_file)
		if not second_text:
			skipped_files_count = skipped_files_count +1
			continue

		# print(f"Length of the second document {len(bytes(second_text, 'utf-8'))}")

		texts_concat = first_text + second_text
		# print(f"Length of the two text combined is {len(bytes(texts_concat, 'utf-8'))}")

		# now doing gzip operation on each option


		zipped_second_text = gzip.compress(bytes(second_text,'utf-8'))
		# print(f"Length of the zipped second document {len(zipped_second_text)}")

		zipped_both_texts = gzip.compress(bytes(texts_concat,'utf-8'))
		# print(f"Length of the zipped first+second documents {len(zipped_both_texts)}")

		# calculating some substraction values between different combinations
		
		# print(f"Second document compression substraction result: {len(bytes(second_text, 'utf-8')) - len(zipped_second_text)}")

		# print(f"Both documents substraction result (focusing on the first document): {len(zipped_both_texts) - len(zipped_first_text)}")
		# print(f"Both documents substraction result (focusing on the second document): {len(zipped_both_texts) - len(zipped_second_text)}")

		## What if we want to focus on both documents and not a specific one (Jensen-Shannon alike)
		both_texts = zipped_first_text + zipped_second_text
		combined_distance = len(both_texts) - len(zipped_both_texts)
		print(f"second_file {second_file} distance: {combined_distance}")

end_time = datetime.datetime.now()
print(f"Skipped {skipped_files_count}/{overall_files_count} files. start_time {start_time} end_time {end_time}, overall seconds: {(end_time - start_time).total_seconds()}")
print("FIN!")
