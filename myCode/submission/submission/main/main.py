import time
import json
import gzip
import ntpath
import os
from sortedcontainers import SortedDict
from scipy.spatial import distance
import itertools
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score
import ast

dir_path = os.path.dirname(os.path.realpath(__file__))
full_path_for_current_distances_file = os.path.join(dir_path,"articles_ids_to_distance.json")
articles_ids_to_distance = dict()
MAX_CLUSTERS_NUM = 3

def find_k_nearest_neighbors(given_id, k):
	global articles_ids_to_distance
	given_distance_tuple = articles_ids_to_distance[given_id]
	nearest_neighbors_distance_to_id = SortedDict()
	for article_id, distance_tuple in articles_ids_to_distance.items():
		if(article_id != given_id):
			dst = -1*distance.euclidean(given_distance_tuple, distance_tuple) #Multiplying by (-1) since the metric we chose gives high values for similar articles
			nearest_neighbors_distance_to_id.setdefault(dst, []).append(article_id)
	k_nearset = SortedDict(itertools.islice(nearest_neighbors_distance_to_id.items(), k))
	neighbors_until_now = 0
	print('Note that by the metric we chose, the higher the "distance" the similar the 2 articles are')
	print(f"Nearest {k} neighbors to {given_id}:")
	for neighbor_distance, article_ids in k_nearset.items():
		if neighbors_until_now>=k:
			break
		neighbors_until_now = neighbors_until_now + len(article_ids)
		print(f"Distance: {round(-1*neighbor_distance,2)} {'article id' if len(article_ids)==1 else 'article ids'}: {article_ids}")



def part1():
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
	global articles_ids_to_distance
	articles_ids_to_distance = json.loads(distances_data)

	find_k_nearest_neighbors(second_article_id, k)



def part2():
	print("Welcome to part 2 - finding the best k for k-clustering (based on average silhouette score)")
	full_path_for_current_distances_to_ids_file = os.path.join(dir_path,'distance_to_articles_ids.json')

	with open(full_path_for_current_distances_to_ids_file, 'r') as myfile:
	    distance_to_articles_ids=json.load(myfile)
	# print(f'finished loading distance_to_articles_ids')
	X = distance_to_articles_ids.keys()
	X = list(map(ast.literal_eval, X))
	best_cluster_num_to_silhouette = (-2, -2)
	X = np.array(X)
	info_for_best_k = dict()
	for clusters_num in range(2,MAX_CLUSTERS_NUM+1):
		print(f"Computing {clusters_num} clusters")

		kmeans = KMeans(n_clusters=clusters_num)
		kmeans.fit(X)
		y_kmeans = kmeans.predict(X)

		silhouette_avg = silhouette_score(X, y_kmeans)
		print(f"For {clusters_num} clusters the silhouette average is {silhouette_avg}")
		if(best_cluster_num_to_silhouette[1]<silhouette_avg):
			best_cluster_num_to_silhouette = (clusters_num, silhouette_avg)
			info_for_best_k["y_kmeans"] = y_kmeans
			info_for_best_k["centers"] = kmeans.cluster_centers_

	print(f"Highest silhouette score {best_cluster_num_to_silhouette[1]} is achieved in {best_cluster_num_to_silhouette[0]} clusters, plotting graph for {best_cluster_num_to_silhouette[0]} clusters")

	plt.scatter(X[:, 0], X[:, 1], c=info_for_best_k["y_kmeans"], s=50, cmap='viridis')
	plt.scatter(info_for_best_k["centers"][:, 0], info_for_best_k["centers"][:, 1], c='black', s=200, alpha=0.5)
	plt.show()


def main():
    print("Hi & welcome to ex2 in AdvancedML course")
    part1()
    part2()


if __name__ == '__main__':
    main()


