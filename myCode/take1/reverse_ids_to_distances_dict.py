import json

distance_to_articles_ids = dict()
full_path_for_current_distances_file = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\articles_ids_to_distance.json'
with open(full_path_for_current_distances_file, 'r') as myfile:
    distances_data=myfile.read()
articles_ids_to_distance = json.loads(distances_data)

for article_id, distance in articles_ids_to_distance.items():
	distance_tuple = str(tuple(distance))
	existing_ids = list()
	# if distance in distance_to_articles_ids:
	# 	existing_ids = distance_to_articles_ids[distance]
	existing_ids = distance_to_articles_ids.setdefault(distance_tuple, []).append(article_id)
	# existing_ids.append(article_id)
	# distance_to_articles_ids[distance] = existing_ids
	# print(f"article_id {article_id} distance {distance}")
print(f"distance_to_articles_ids {distance_to_articles_ids}")
print(f"len(distance_to_articles_ids) {len(distance_to_articles_ids)}")
# for distance, article_ids in distance_to_articles_ids.items():
# 	if len(article_ids)>1:
# 		print(f"distance {distance} article_ids {article_ids}")

out_file = "distance_to_articles_ids.json"
print(f"Writing to out file {out_file} - Start")
with open(out_file, 'w') as file:
     json.dump(distance_to_articles_ids, file, indent=4)

print(f"Writing to out file {out_file} - End")


