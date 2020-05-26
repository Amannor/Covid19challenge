import json
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score
import ast
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
full_path_for_current_distances_file = os.path.join(dir_path,'distance_to_articles_ids.json')

with open(full_path_for_current_distances_file, 'r') as myfile:
    distance_to_articles_ids=json.load(myfile)
print(f'finished loading distance_to_articles_ids')
X = distance_to_articles_ids.keys()
X = list(map(ast.literal_eval, X))
best_cluster_num_to_silhouette = (-2, -2)
X = np.array(X)
for clusters_num in range(2,11):
	print(f"Computing {clusters_num} clusters")

	kmeans = KMeans(n_clusters=clusters_num)
	kmeans.fit(X)
	y_kmeans = kmeans.predict(X)

	plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

	centers = kmeans.cluster_centers_
	plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
	# plt.show()

	silhouette_avg = silhouette_score(X, y_kmeans)
	print(f"for {clusters_num} clusters the silhouette average is {silhouette_avg}")
	if(best_cluster_num_to_silhouette[1]<silhouette_avg):
		best_cluster_num_to_silhouette = (clusters_num, silhouette_avg)
print(f"Highest silhouette score {best_cluster_num_to_silhouette[1]} is achieved in {best_cluster_num_to_silhouette[0]} clusters")
