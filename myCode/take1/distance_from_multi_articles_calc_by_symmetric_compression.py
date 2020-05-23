import os
import sys
import json
import gzip
import datetime
import ntpath

start_time = datetime.datetime.now()
overall_files_count = 0
skipped_files_count = 0
ids = set()
text_basis = []
articles_ids_to_distance = dict()

def is_paper_id_in_ids(raw_id):
	cur_ids = map(str.strip, raw_id.split(";"))
	cur_ids = list(filter(lambda x: x in ids, cur_ids))
	return len(cur_ids)>0

def extract_text(file_path):
    with open(file_path, 'r') as f:
        cur_file_as_dict = json.load(f)
    list_of_texts = cur_file_as_dict['body_text']
    full_text = ''
    if(is_paper_id_in_ids(cur_file_as_dict['paper_id'])):
    	full_text = ' '.join([lof['text'] for lof in list_of_texts])
    return full_text

def init_ids():
	#Init the set of articles ids
	ids_file_path = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\nonempty_ids_of_full_text_articles.txt'
	with open(ids_file_path) as infile:
		for line in infile:
			if line:
				ids.update(map(str.strip, line.split(";")))

def init_basis():
	basis_paths = [r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pdf_json\c63c4d58d170136b8d3b5a66424b5ac3f73a92d9.json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pdf_json\b2897e1277f56641193a6db73825f707eed3e4c9.json']
	for basis_path in basis_paths:
		text = extract_text(basis_path)
		if text:
			text_basis.append(text)
	print(f"len(text_basis) {len(text_basis)}")


def init():
	init_ids()
	init_basis()
init()


## Configurations
data_paths = [r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\biorxiv_medrxiv\biorxiv_medrxiv\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pmc_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pmc_json',r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pmc_json']


for data_path in data_paths:
	## Extracting the text
	files_found = [f for f in os.listdir(data_path) if f.endswith('.json')]
	files_found_full_path = [os.path.join(data_path, f) for f in files_found]
	files_path_subset = files_found_full_path[0:len(files_found)]

	overall_files_count = overall_files_count+len(files_path_subset)
	for second_document_idx in range(len(files_path_subset)):
	
		second_file = files_path_subset[second_document_idx]
		second_text = extract_text(second_file)
		if not second_text:
			skipped_files_count = skipped_files_count +1
			continue

		# now doing gzip operation on each option
		zipped_second_text = gzip.compress(bytes(second_text,'utf-8'))
		second_article_id = os.path.splitext(ntpath.basename(second_file))[0]
		distances_to_basis = []
		for first_text in text_basis:
			zipped_first_text = gzip.compress(bytes(first_text,'utf-8'))
			texts_concat = first_text + second_text

			zipped_both_texts = gzip.compress(bytes(texts_concat,'utf-8'))
		
			# What if we want to focus on both documents and not a specific one (Jensen-Shannon alike)
			both_texts = zipped_first_text + zipped_second_text
			combined_distance = len(both_texts) - len(zipped_both_texts)
			distances_to_basis.append(combined_distance)
		cur_distance = tuple(distances_to_basis)
		print(f"second_file {second_file} distance: {cur_distance}")
		articles_ids_to_distance[second_article_id] = cur_distance

end_time = datetime.datetime.now()
print(f"Skipped {skipped_files_count}/{overall_files_count} files. start_time {start_time} end_time {end_time}, overall seconds: {(end_time - start_time).total_seconds()}")

out_file = "articles_ids_to_distance.json"
print(f"Writing to out file {out_file} - Start")
with open(out_file, 'w') as file:
     json.dump(articles_ids_to_distance, file, indent=4)

print(f"Writing to out file {out_file} - End")

print("FIN!")
