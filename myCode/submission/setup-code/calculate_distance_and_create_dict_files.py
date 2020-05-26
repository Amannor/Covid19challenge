import os
import sys
import json
import gzip
import datetime
import ntpath

IDS_FILE_PATH = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\submission\setup-code\nonempty_ids_of_full_text_articles.txt'
BASIS_PATHS = [r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\comm_use_subset\comm_use_subset\pdf_json\c63c4d58d170136b8d3b5a66424b5ac3f73a92d9.json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\custom_license\custom_license\pdf_json\b2897e1277f56641193a6db73825f707eed3e4c9.json']
DATA_PATHS = [r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\biorxiv_medrxiv\biorxiv_medrxiv\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\comm_use_subset\comm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\comm_use_subset\comm_use_subset\pmc_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\custom_license\custom_license\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\custom_license\custom_license\pmc_json',r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pmc_json']
OUT_FILE_IDS_TO_DISTANCES = 'articles_ids_to_distance.json'
OUT_FILE_DISTANCES_TO_IDS = 'distance_to_article_ids.json'

start_time = datetime.datetime.now()
overall_files_count = 0
skipped_files_count = 0
ids = set()
text_basis = []
articles_ids_to_distance = dict()
distance_to_articles_ids = dict()


def get_article_id_from_full_path(full_path):
	'''
	Returns the sha of an article (equal to filename without the extension)
	'''
	return os.path.splitext(ntpath.basename(full_path))[0]

def is_paper_id_in_ids(raw_id):
	'''
	Returns true iff given article_id is in the (preset) set of ids of full-text articles
	'''
	cur_ids = map(str.strip, raw_id.split(";"))
	cur_ids = list(filter(lambda x: x in ids, cur_ids))
	return len(cur_ids)>0

def extract_text(file_path):
	'''
	Extracts and returns the full-text of the article in the given file_path
	Note: If the article appear as a full-text article, this method will return an empty string
	'''
	with open(file_path, 'r') as f:
		cur_file_as_dict = json.load(f)
	list_of_texts = cur_file_as_dict['body_text']
	full_text = ''
	if(is_paper_id_in_ids(cur_file_as_dict['paper_id'])):
		full_text = ' '.join([lof['text'] for lof in list_of_texts])
	return full_text

def init_ids():
	'''
	Init the set of articles ids that have a full text (according the respective column in metadata.csv)
	'''
	
	with open(IDS_FILE_PATH) as infile:
		for line in infile:
			if line:
				ids.update(map(str.strip, line.split(";")))

def init_basis():
	'''
	Inits the elements of the basis
	'''
	
	basis_ids = list()
	for basis_path in BASIS_PATHS:
		text = extract_text(basis_path)
		if text:
			basis_member = dict()
			basis_member["BASIS_FULL_TXT"] = text
			basis_member["BASIS_ZIPPED_TXT"] = gzip.compress(bytes(text,'utf-8'))
			text_basis.append(basis_member)
			basis_ids.append(get_article_id_from_full_path(basis_path))
	print(f"Basis members ids: {basis_ids}")

def init():
	'''
	Init function
	'''
	print("Initializing ids of articles with full text")
	init_ids()
	print("Initializing basis")
	init_basis()

def populate_distances():
	print("populate_distances")
	global overall_files_count
	global skipped_files_count
	global articles_ids_to_distance
	for data_path in DATA_PATHS:
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
			zipped_second_text = gzip.compress(bytes(second_text,'utf-8'))
			second_article_id = os.path.splitext(ntpath.basename(second_file))[0]
			distances_to_basis = []
			for basis_member in text_basis:
				first_text = basis_member["BASIS_FULL_TXT"]
				zipped_first_text = basis_member["BASIS_ZIPPED_TXT"]
				texts_concat = first_text + second_text

				zipped_both_texts = gzip.compress(bytes(texts_concat,'utf-8'))
			
				# What if we want to focus on both documents and not a specific one (Jensen-Shannon alike)
				both_texts = zipped_first_text + zipped_second_text
				combined_distance = len(both_texts) - len(zipped_both_texts)
				distances_to_basis.append(combined_distance)
			cur_distance = tuple(distances_to_basis)
			print(f"second_file {second_file} distance: {cur_distance}")
			articles_ids_to_distance[second_article_id] = cur_distance
			existing_ids = distance_to_articles_ids.setdefault(str(cur_distance), []).append(second_article_id)


def write_to_out_files():
	print(f"Writing to out file {OUT_FILE_IDS_TO_DISTANCES} - Start")
	with open(OUT_FILE_IDS_TO_DISTANCES, 'w') as file:
		json.dump(articles_ids_to_distance, file, indent=4)
	print(f"Writing to out file {OUT_FILE_IDS_TO_DISTANCES} - End")

	print(f"Writing to out file {OUT_FILE_DISTANCES_TO_IDS} - Start")
	with open(OUT_FILE_DISTANCES_TO_IDS, 'w') as file:
		json.dump(distance_to_articles_ids, file, indent=4)
	print(f"Writing to out file {OUT_FILE_DISTANCES_TO_IDS} - End")

init()
populate_distances()
write_to_out_files()
end_time = datetime.datetime.now()
print(f"Skipped {skipped_files_count}/{overall_files_count} files. start_time {start_time} end_time {end_time}, overall seconds: {(end_time - start_time).total_seconds()}")