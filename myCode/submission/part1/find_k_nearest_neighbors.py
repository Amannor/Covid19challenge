import json
import gzip
import ntpath
import os
from sortedcontainers import SortedDict
from scipy.spatial import distance
import itertools

def find_k_nearest_neighbors(given_id):
	given_distance_tuple = articles_ids_to_distance[given_id]
	nearest_neighbors_distance_to_id = SortedDict()
	for article_id, distance_tuple in articles_ids_to_distance.items():
		if(article_id != given_id):
			dst = distance.euclidean(given_distance_tuple, distance_tuple)
			nearest_neighbors_distance_to_id.setdefault(dst, []).append(article_id)
	k_nearset = SortedDict(itertools.islice(nearest_neighbors_distance_to_id.items(), k))
	neighbors_until_now = 0
	print(f"nearest {k} neighbors to {given_id}:")
	for neighbor_distance, article_ids in k_nearset.items():
		if neighbors_until_now>=k:
			break
		neighbors_until_now = neighbors_until_now + len(article_ids)
		print(f"Distance: {round(neighbor_distance,2)} {'article id' if len(article_ids)==1 else 'article ids'}: {article_ids}")

dir_path = os.path.dirname(os.path.realpath(__file__))
full_path_for_current_distances_file = os.path.join(dir_path,"articles_ids_to_distance.json")


print("Welcome to part 1 - finding the k nearest articles for a given article + their distance")
print("Please enter full path of article")
second_file_full_path = input() #e.g.: C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pdf_json\ffdd6ba963bcbed1b9e7a293b06529bb4da989b6.json
print("Please enter a K fo your choice")
k = -1
while k<0:
	try:
	   k = int(input())
	   if(k<0):
	   	print("k must be a nonegative  int!")
	except ValueError:
	   print("k must be a nonegative  int!")

second_article_id = os.path.splitext(ntpath.basename(second_file_full_path))[0]
with open(full_path_for_current_distances_file, 'r') as myfile:
    distances_data=myfile.read()
articles_ids_to_distance = json.loads(distances_data)

find_k_nearest_neighbors(second_article_id)


