import json
import gzip
import ntpath
import os
from sortedcontainers import SortedDict
from scipy.spatial import distance
import itertools

text_basis = []
full_path_for_current_distances_file = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\articles_ids_to_distance.json'

print("Welcome to part 1 - finding the k nearest articles for a given article + their distance")
print("Please enter full path of article")
second_file = input() #e.g.: C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pdf_json\ffdd6ba963bcbed1b9e7a293b06529bb4da989b6.json
print("Please enter a K fo your choice")
k = -1
while k<0:
	try:
	   k = int(input())
	   if(k<0):
	   	print("k must be a nonegative  int!")
	except ValueError:
	   print("k must be a nonegative  int!")

def extract_text(file_path):
    with open(file_path, 'r') as f:
        cur_file_as_dict = json.load(f)
    list_of_texts = cur_file_as_dict['body_text']
    full_text = ' '.join([lof['text'] for lof in list_of_texts])
    return full_text

def init_basis():
	basis_paths = [r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pdf_json\c63c4d58d170136b8d3b5a66424b5ac3f73a92d9.json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pdf_json\b2897e1277f56641193a6db73825f707eed3e4c9.json']
	for basis_path in basis_paths:
		text = extract_text(basis_path)
		if text:
			text_basis.append(text)
	print(f"len(text_basis) {len(text_basis)}")


init_basis()

def find_k_nearest_neighbors(given_article_id_to_distance):
	given_id = list(given_article_id_to_distance.keys())[0]
	given_distance_tuple = given_article_id_to_distance[given_id]
	nearest_neighbors_distance_to_id = SortedDict()
	for article_id, distance_tuple in articles_ids_to_distance.items():
		if(article_id != given_id):
			dst = distance.euclidean(given_distance_tuple, distance_tuple)
			nearest_neighbors_distance_to_id[dst] = article_id
	print(f"nearest_k_neighbors_distance_to_id {SortedDict(itertools.islice(nearest_neighbors_distance_to_id.items(), k))}")




second_text = extract_text(second_file)

# now doing gzip operation on each option
zipped_second_text = gzip.compress(bytes(second_text,'utf-8'))
second_article_id = ntpath.basename(second_file)
distances_to_basis = []
cur_article_id_to_distance = dict()
for first_text in text_basis:
	zipped_first_text = gzip.compress(bytes(first_text,'utf-8'))
	texts_concat = first_text + second_text

	zipped_both_texts = gzip.compress(bytes(texts_concat,'utf-8'))

	# What if we want to focus on both documents and not a specific one (Jensen-Shannon alike)
	both_texts = zipped_first_text + zipped_second_text
	combined_distance = len(both_texts) - len(zipped_both_texts)
	distances_to_basis.append(combined_distance)
cur_distance = tuple(distances_to_basis)
cur_article_id_to_distance[os.path.splitext(ntpath.basename(second_file))[0]] = cur_distance
print(f"{cur_article_id_to_distance}")

with open(full_path_for_current_distances_file, 'r') as myfile:
    distances_data=myfile.read()
articles_ids_to_distance = json.loads(distances_data)

find_k_nearest_neighbors(cur_article_id_to_distance)



