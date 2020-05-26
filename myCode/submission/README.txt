Advanced Machine Learning - IDC, May 2020

Exercise 2 - Corona Papers
==========================
Background
----------
The problem of finding a sensible way to semantically interpet large-scale text corpuses has been (and still is) a fascinating & challenging one.In this exercise I'll suggest a very basic & somewhat
simplistic way to tackle this, in the confines of the requirements of this specific task.
What I have decided to do is:
(I)   To choose the symmetric distance calculation method (hereinafter "the metric")
(II)  To arbitrarily choose 2 articles that'll serve as the basis for the "vector space" that is the set of all the full text articles (represented by the metric)
(III) For each article I'll calculate a 2-dimensional coordinate - the 1st memeber will be the distance from the 1st memeber of the basis - and same for each memeber of the basis
(IV)  Now that every article is representedby a n-dimensional coordinate (in our case 2), every distance-based question (e.g. k nearest neighbors, k clustering etc.) has a "shelf" algorithm + implementation.

Caveats
-------
The dimension of the basis, as well as its memebers, the compression algorithm that makes up the metric were chosen, as stated, arbitrarily and as such there's no guarantee that they're in any way
sufficient. There's obvisouly room for improvements (see below). Since this is the case, there's little reason to believe any real-world insights will be made from this specific implementation -
and this serves as simply a way to incorporate compression algorithms into text-analysis.


Part 1
------
To Run: run the file find_k_nearest_neighbors.py
Part 2
------


Pros & cons of selected method
------------------------------


Future possible improvements & directions
-----------------------------------------

Explanation on files
README.txt - this file