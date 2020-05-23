import datetime

start_time = datetime.datetime.now()
ids_file_path = r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\nonempty_ids_of_full_text_articles.txt'
lines_num = 0
ids = set()
with open(ids_file_path) as infile:
    for line in infile:
        if line:
        	lines_num=lines_num+1
        	ids.update(map(str.strip, line.split(";")))

end_time = datetime.datetime.now()
print(f"Finished in {(end_time - start_time).total_seconds()} seconds, lines_num {lines_num} len(ids) {len(ids)}")
