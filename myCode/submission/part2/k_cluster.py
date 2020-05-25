import json
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import silhouette_score
import ast


full_path_for_current_distances_file = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\distance_to_articles_ids.json'
with open(full_path_for_current_distances_file, 'r') as myfile:
    distance_to_articles_ids=json.load(myfile)
print(f'finished loading distance_to_articles_ids')
X = distance_to_articles_ids.keys()
X = list(map(ast.literal_eval, X))
# print(f"X[0] {X[0]}")
# print(f"type(X[0]) {type(X[0])}")
# v = ast.literal_eval(X[0])
# print(f"type(v) {type(v)}")

# X = list(map(lambda d: tuple(d), distance_to_articles_ids.keys()))
X = np.array(X)
# print(f"X {X}")
for clusters_num in range(2,10):

	kmeans = KMeans(n_clusters=clusters_num)
	kmeans.fit(X)
	y_kmeans = kmeans.predict(X)

	plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')

	centers = kmeans.cluster_centers_
	plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5)
	# plt.show()

	# clusterer = KMeans(n_clusters=clusters_num, random_state=10)
	# cluster_labels = clusterer.fit_predict(X)
	silhouette_avg = silhouette_score(X, y_kmeans)
	print(f"clusters_num {clusters_num} silhouette_avg {silhouette_avg}")
