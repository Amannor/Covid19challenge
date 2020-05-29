Advanced Machine Learning - IDC, May 2020

Exercise 2 - Corona Papers
==========================
Background
----------
The problem of finding a sensible way to semantically interpret large-scale text corpuses has been (and still is) a fascinating &
challenging one. In this exercise I'll suggest a very basic & somewhat simplistic way to tackle this, in the confines of the
requirements of this specific task.

What I have decided to do is:
(I)   Choose the symmetric distance calculation method presented by Abrahami in his notebook ("Jensen–Shannon" like,
	  hereinafter "the metric").
(II)  Arbitrarily choose 2 articles that'll serve as the basis for the "vector space" that is the set of all the full text
	  articles (represented by the metric).
(III) For each article I'll calculate a 2-dimensional coordinate - the 1st member will be the distance from the 1st member of
      the basis - and same for each member of the basis.
(IV)  Now that every article is represented by an n-dimensional coordinate (in our case n=2), every distance-based question
      (e.g. k nearest neighbors, k clustering etc.) has a "shelf" algorithm + implementation.

Caveats
-------
The dimension of the basis, as well as its members and the compression algorithm that makes up the metric were chosen, as
stated, arbitrarily. As such there's no guarantee that they're in any way sufficient. There's obvisouly room for improvements
(see below). Since this is the case, there's little reason to believe any real-world insights will be made from this specific
implementation - and this serves simply as a way to incorporate compression algorithms into text-analysis.

Main
----
The main folder is one long python file (with a main entry-point) that includes my implementation for parts 1 & 2.
It's ready to be run as is. Also, one can run each part individually (see below on each part's explanation).

Part 1
------
To Run: run the file find_k_nearest_neighbors.py and enter what the program asks (first the full path of the article and then
the desired k).

Part 2
------
To Run: run the file k_cluster.py. The code iterates through k from 2 to MAX_CLUSTERS_NUM (default value is 5, can be changed
manually in the file). For each k, the code outputs the average silhouette score for that k. Finally it plots the k cluster for
which the average silhouette score was the best (i.e. the highest).

Pros & cons of the selected method
----------------------------------
Pros
----
 - Easy to implement & visualize
 - The metric chosen is symmetric and hence is independent of order of articles
 - The code was written to easily support any (reasonable) finite number of members as the basis that's used for distance-calculating

Cons
----
- The metric isn't intuitive (for once, the closer the articles, the higher the numerical value of their distance is)
- The correct dimension & composition of the basis is TBD and more so - it lacks a clear method of formulating what constitues
  a "good" basis choice
- The method chosen for part 2 (k-clusters) was selected as somewhat of a "default" option without a "good enough" comparison to
  other alternatives
- The method chosen in part 2 for evaluating each of the k-clusters (average silhouette) wasn't compared to their similar
  evaluation methods (e.g. Dunn-index)


Future possible improvements & directions
-----------------------------------------
- The number and composition of the basis should be improved. Since going over the entire full text of all the papers can be
  cumbersome & will also in a way defeat the purpose of this exercise, other methods should be considered. These include, but
  are not limited to, classify by the abstract of each article, perhaps looking deeper into the metadata of each article,
  looking for similar patterns \ subjects etc.
 
- Other compression methods should be considered (at least those which have a straight-forward support in python).

- Other metrics should be considered. Ideally one that's "intuitive" (i.e. symmetric, transitive & maintaines the triangle
  inequality)


Included files
--------------
*Note:
-----
(I) Files with the same names are exact copies of each other, and are just held in different folders so as to make the code
    inside them self-contained.
(II)For each article file, the article id is defined as the file name without the extension. Given a full path in python,
    the id is: os.path.splitext(ntpath.basename(full_path))[0]

Files
-----

 - README.txt - this file
 
 - requirements.txt - contains all of the relavant python packages needed to run the code. They can be easily installed by
   running "pip install requirements.txt"
   
 - setup-code (folder)
   -------------------
   *This folder contains the code needed to setup the data files used by the code that implements the parts hereinafter
   
   - calculate_distance_and_create_dict_files.py - The code that goes over all of the articles that have full text and creates
     the json files used hereinafer. It uses hard coded locations & filenames - please see the consts at the top of the file 
	 (written in upper case) for details.
	 
   - nonempty_ids_of_full_text_articles.txt - contains a list of the ids of all of the articles that contain full text.
     This was done by filtering the given metadata.csv file by the column name "full_text" and taking only the rows that have
	 either of the following values: biorxiv_medrxiv, comm_use_subset, noncomm_use_subset, custom_license.
	 In case the row contained multiple ids, they were delimited by ";" and treated as seperate entries.
	 
   - articles_ids_to_distance.json - Contains a json dictionary of an article id to its distance
   
   - distance_to_articles_ids.json - Contains a json dictionary of distance to a list of article ids that have this distance
	 from the basis
	
   
 - main (folder)
   -------------
   - main.py - The main python file. Holds the implementation for parts 1 & 2
   
   - articles_ids_to_distance.json - Contains a json dictionary of an article id to its distance
   
   - distance_to_articles_ids.json - Contains a json dictionary of distance to a list of article ids that have this distance
	 from the basis

 - part1 (folder)
   --------------
   - find_k_nearest_neighbors.py - Holds the implementation for parts 1
   - articles_ids_to_distance.json - Contains a json dictionary of an article id to its distance
   
 - part2 (folder)
   --------------
   - k_cluster.py - Holds the implementation for parts 2 (note you can change the const MAX_CLUSTERS_NUM)
   
   - distance_to_articles_ids.json - Contains a json dictionary of distance to a list of article ids that have this distance
	 from the basis
	 
Appendix - references
---------------------
- Wiki article on silhouette:
  https://en.wikipedia.org/wiki/Silhouette_(clustering)

- Wiki article on dunn index:
  https://en.wikipedia.org/wiki/Dunn_index

- Explanatory page on dunn index:
  https://www.datanovia.com/en/lessons/cluster-validation-statistics-must-know-methods/#dunn-index

   
   