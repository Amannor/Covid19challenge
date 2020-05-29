import json
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score
import ast
import os

MAX_CLUSTERS_NUM = 5

dir_path = os.path.dirname(os.path.realpath(__file__))
full_path_for_current_distances_file = os.path.join(dir_path,'distance_to_articles_ids.json')

with open(full_path_for_current_distances_file, 'r') as myfile:
    distance_to_articles_ids=json.load(myfile)
print(f'finished loading distance_to_articles_ids')
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
