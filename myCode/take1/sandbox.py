import os

data_paths = [r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\biorxiv_medrxiv\biorxiv_medrxiv\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\comm_use_subset\comm_use_subset\pmc_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\custom_license\custom_license\pmc_json',r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pdf_json', r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\articles_with_full_text\noncomm_use_subset\noncomm_use_subset\pmc_json']

END_OF_ABS_PATH = 'articles_with_full_text'
print(END_OF_ABS_PATH)
for data_path in data_paths:
	print(data_path)
	index = data_path.index(END_OF_ABS_PATH) + len(END_OF_ABS_PATH)+1 ##for Trailing \
	print(data_path[index:]) 
	print(os.path.join(r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\output',data_path[index:])) 
	os.makedirs(os.path.join(r'C:\idc\AdvancedML\ex2_and_relevant_lectures\myCode\take1\output',data_path[index:]))
